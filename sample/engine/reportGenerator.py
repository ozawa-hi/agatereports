try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

import datetime
import re

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
#from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Paragraph, Table, TableStyle, KeepInFrame
from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from PIL import Image

from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps, usps4s, common
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# from reportlab.lib.fonts import addMapping
from reportlab import rl_config

from agatereports.sample.engine.jrxml2json import parse_jrxml
# from agatereports.jrxml.constants import constants
from agatereports.sample.adapters.MysqlAdapter import MysqlAdapter
from agatereports.sample.adapters.PostgresqlAdapter import PostgresqlAdapter
import psycopg2
from psycopg2.extras import DictCursor
from agatereports.sample.adapters.CSVAdapter import CSVAdapter
import collections

try:
    from agatereports.java import java_formatter
    java = True
except:
    java = False

# TODO need to break this file into smaller files.
# TODO need performance improvement.

report = {}      # report information
properties = {}  # report properties
variables = {}   # variables


def initialize():
    global report, properties, variables

    report = {}
    properties = {}
    variables = {   # initial system variables
        'PAGE_NUMBER': {'value': 1, 'class': 'java.lang.Integer'},
        'MASTER_CURRENT_PAGE': {'value': None, 'class': 'java.lang.Integer'},
        'MASTER_TOTAL_PAGES': {'value': None, 'class': 'java.lang.Integer'},
        'COLUMN_NUMBER': {'value': 1, 'class': 'java.lang.Integer'},
        'REPORT_COUNT': {'value': 0, 'class': 'java.lang.Integer'},
        'PAGE_COUNT': {'value': 0, 'class': 'java.lang.Integer'},
        'COLUMN_COUNT': {'value': 0, 'class': 'java.lang.Integer'}
    }


def create_canvas(pdf_filename):
    global report

    default_page_width, default_page_height = A4    # set default page siae to A4
    global page_width, page_height, cur_y

    page_width= report.get('pageWidth', default_page_width)
    page_height = report.get('pageHeight', default_page_height)
    cur_y = page_height

    report['canvas'] = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))
    report['canvas'].setAuthor('AgateReports')
    report['canvas'].setTitle(report.get('name', 'sample report'))
    report['canvas'].setSubject(report.get('name', 'sample report'))


def set_fonts(fonts_list):
    """
    Register specified fonts and font families to canvas.
    :param fonts_list: list of fonts and font families to register
    """
    global report

    # TODO scan jrxml and try to automatically load fonts

    report['available_fonts'] = []
    if fonts_list is not None:
        for font in fonts_list:
            font_path = font.get('font_path')
            if type(font_path) == list:
                rl_config.TTFSearchPath.extend(font_path)
            font_filename = font.get('font_filename')
            font_list = font.get('fonts')
            if font_filename is not None and font_list is not None:
                if type(font_list) is str:
                    try:
                        pdfmetrics.registerFont(TTFont(font_list, font_filename))
                        report['available_fonts'].append(font_list)
                    except:  # if font files is not found, output error and skip it.
                        print('font not found. font name:' + name + ' file name:' + font_filename)
                elif type(font_list) is list:
                    for font_reg in font_list:
                        index = font_reg.get('index')
                        name = font_reg.get('name')
                        if name is not None:
                            if index is not None:
                                try:
                                    pdfmetrics.registerFont(TTFont(name, font_filename, subfontIndex=index))
                                    report['available_fonts'].append(name)
                                except: # if font files is not found, output error and skip it.
                                    print('font not found. font name:' + name + ' file name:' + font_filename)
                            else:
                                try:
                                    pdfmetrics.registerFont(TTFont(name, font_filename))
                                    report['available_fonts'].append(name)
                                except: # if font files is not found, output error and skip it.
                                    print('font not found. font name:' + name + ' file name:' + font_filename)
            font_family = font.get('font-family')
            if font_family is not None:
                if font_family.get('name') is not None and font_family.get('normal') is not None\
                        and font_family.get('bold') is not None and font_family.get('italic') is not None\
                        and font_family.get('boldItalic') is not None:
                    pdfmetrics.registerFontFamily(font_family.get('name'), normal=font_family.get('normal'),
                                                  bold=font_family.get('bold'),
                                                  italic=font_family.get('italic'),
                                                  boldItalic=font_family.get('boldItalic'))


def write_to_file():
    """
    Start a new page and save current canvas to a file.
    """
    global report

    # save page to file
    report['canvas'].showPage()  # start a new page
    report['canvas'].save()      # save to a file


def process_property_band(element):
    """
    Read jrxml properties elements and set to 'properties' dictionary.
    :param element: jrxml properties element
    """
    global properties

    add_attr2attributes(element, properties)


def process_query_string_band(element):
    """
    Read from jrxml queryString element and query a datasource.
    :param element:
    """
    global report

    sql_stmt = element.get('value')
    if sql_stmt is not None:
        sql_stmt = sql_stmt.strip()
        report['field_names'] = report['main_datasource'].execute_query(sql_stmt)


def process_field_band(element):
    """
    Process jrxml field element.
    Add field names and it's class (datatype) info to 'field_dict' in global 'report' variable.
    :param element:
    :return:
    """
    global report

    field_attr = element.get('attr')
    name = field_attr.get('name')
    datatype = field_attr.get('class')

    if report.get('field_dict') is None:
        report['field_dict'] = dict()
    report['field_dict'][name] = datatype


def process_variable_band(element):
    """
    Process jrxml variable element.
    :param element:
    """
    global variables

    pass    # currently not supported


def process_background_band(element):
    """
    Process jrxml background element.
    :param element:
    """
    pass    # currently not supported


def process_group_band(element):
    # print(element)
    pass

def process_title_band(element=None):
    process_band_element(element)


def page_header_band(element=None):
    global report

    if element is None:
        page_header =  report.get('pageHeader')
        if page_header is not None:
            element = report['pageHeader'][0]['pageHeader']
    process_band_element(element)


def column_header_band(element=None):
    global report

    if element is None:
        column_header = report.get('columnHeader')
        if column_header is not None:
            element = report['columnHeader'][0]['columnHeader']
    process_band_element(element)


def get_band_height(element):
    return float(element['child'][0]['band']['attr']['height'])


def calc_column_footer_band_height():
    global report
    if report.get('columnFooter') is None:
        return 0
    else:
        return get_band_height(report['columnFooter'][0]['columnFooter'])


def column_footer_band(element=None):
    global report

    if element is None:
        column_footer = report.get('columnFooter')
        if column_footer is not None:
            element = report['columnFooter'][0]['columnFooter']
    process_band_element(element)


def calc_page_footer_band_height():
    global report
    if report.get('pageFooter') is None:
        return 0
    else:
        return get_band_height(report['pageFooter'][0]['pageFooter'])


def page_footer_band(element=None):
    global report

    if element is None:
        page_footer = report.get('pageFooter')
        if page_footer is not None:
            element = report['pageFooter'][0]['pageFooter']
    process_band_element(element)


def summary_band(element):
    process_band_element(element)


def text_element(element):
    # process_text(element)
    pass


def process_reportElement(element):
    """
    Set attributes of "reportElement" to a dictionary.
    :param element:
    :return:
    """
    text_settings = element.get('attr')
    attributes = {
        'x': int(text_settings.get('x')) + report['leftMargin'],
        'y': int(text_settings.get('y')),
        'height': int(text_settings.get('height')),
        'width': int(text_settings.get('width')),
        'forecolor': text_settings.get('forecolor'),
        'backcolor': text_settings.get('backcolor'),
        'mode': text_settings.get('mode')  # 'Opaque': show
    }
    return attributes


def process_graphicElement(element, attributes):
    """
    Process jrxml graphicElement.
    Get attributes on graphicElement.
    :param element: current jrxml element being processes.
    :param attributes: current dictionary of attributes.
    :return: attributes with attributes of pen under graphicElements.
    """
    if len(element) > 1:
        graphic_element = element[1].get('graphicElement')  # get graphicElement
        if graphic_element is not None:
            pen = graphic_element.get('child')
            if pen is not None:
                add_attr2attributes(pen[0].get('pen'), attributes)
    return attributes


"""
List of possible line styles.
"""
line_style_dict = {
    'Solid': (1),
    'Dashed': (6,3),
    'Dotted': (1,2),
    'Double': (1)
}


def set_pen_attr(element, attributes):
    """
    Set pen attributes.
    :param element:
    :param attributes:
    :return:
    """
    pen_attr = element.get('attr')
    if pen_attr is None:
        return {}
    else:
        return {
            'lineStyle': pen_attr.get('lineStyle'),
            'lineWidth': float(pen_attr.get('lineWidth', '0')),
            'lineColor': pen_attr.get('lineColor')
        }


def strip_fname(name):
    """
    strip wrapper (e.g. F${}, V${}, P${}) from name.
    :param element: name to string.
    :return: element name without wrapper.
    """
    return name[3:-1]


def draw_line(x1, y1, x2, y2, line_style, line_width, line_color):
    """
    Draw a line on canvas.
    :param x1: start x coordinate
    :param y1: start y coordinate
    :param x2: end x coordinate
    :param y2: end y coordinate
    :param line_style: line style
    :param line_width: line width
    :param line_color: line color in #FFFFFF format
    """
    global report

    report['canvas'].saveState()

    report['canvas'].setDash(line_style_dict.get(line_style, (1)))
    report['canvas'].setLineWidth(line_width)
    if line_color is not None:
        report['canvas'].setStrokeColor(colors.HexColor(line_color))
    report['canvas'].line(x1, y1, x2, y2)
    if line_style == 'Double':  # double line consists of wide solid line with thin white line in between
        report['canvas'].setLineWidth(line_width*0.5)
        report['canvas'].setStrokeColor(colors.HexColor('#FFFFFF'))
        report['canvas'].line(x1, y1, x2, y2)

    report['canvas'].restoreState()


def draw_diagonal_line(attributes, line_style, line_width, line_color):
    """
    Process to jrxml diagonal line.
    :param attributes: line attributes. Attributes from "reportElement" element.
    :param line_style: line style
    :param line_width: line width
    :param line_color: line color
    """
    if attributes.get('direction') is None:  # top down
        draw_line(attributes['x'],
                  report['cur_y'] - attributes['y'],
                  attributes['x'] + attributes['width'],
                  report['cur_y'] - attributes['y'] - attributes['height'],
                  line_style, line_width, line_color)
    else:  # bottom up
        draw_line(attributes['x'],
                  report['cur_y'] - attributes['y'] - attributes['height'],
                  attributes['x'] + attributes['width'],
                  report['cur_y'] - attributes['y'],
                  line_style, line_width, line_color)


def process_line(element, row_data):
    """
    Process jrxml line element.
    :param element: jrxml line element
    """
    line_element = element.get('child')
    if line_element is not None:
        reportElement = process_reportElement(line_element[0].get('reportElement'))  # get reportElement
        # get attributes on line element (e.g. "direction") to determine which direction to draw a line
        add_attr2attributes(element, reportElement)

        # set attributes from following graphicElement
        reportElement = process_graphicElement(line_element, reportElement)

        # set line attributes
        line_style = reportElement.get('lineStyle')
        line_width = float(reportElement.get('lineWidth', '1.0'))
        line_color = reportElement.get('lineColor')

        draw_diagonal_line(reportElement, line_style, line_width, line_color)


def process_box_element(element, attributes):
    """
    Draw borders around a component.
    :param element: jrxml box element
    :param attributes:
    """
    global report

    report['canvas'].saveState()

    borders = element.get('child')
    if borders is not None:
        cell_border = {}
        # find each border line attributes
        for pen_elements in borders:
            for pen_key, pen_value in pen_elements.items():
                if pen_key == 'pen':    # draw all borders
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:    # all borders
                        cell_border['top'] = pen
                        cell_border['left'] = pen
                        cell_border['bottom'] = pen
                        cell_border['right'] = pen
                elif pen_key == 'topPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['top'] = pen
                elif pen_key == 'leftPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['left'] = pen
                elif pen_key == 'bottomPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['bottom'] = pen
                elif pen_key == 'rightPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['right'] = pen
        # draw each border lines
        # draw top
        if cell_border.get('top') is not None:
            draw_line(attributes['x'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'],
                      cell_border['top']['lineStyle'], cell_border['top']['lineWidth'], cell_border['top']['lineColor']
                      )
        # draw left
        if cell_border.get('left') is not None:
            draw_line(attributes['x'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['left']['lineStyle'], cell_border['left']['lineWidth'], cell_border['left']['lineColor']
                      )
        # draw bottom
        if cell_border.get('bottom') is not None:
            draw_line(attributes['x'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['bottom']['lineStyle'], cell_border['bottom']['lineWidth'], cell_border['bottom']['lineColor'])
        # draw right
        if cell_border.get('right') is not None:
            draw_line(attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['right']['lineStyle'], cell_border['right']['lineWidth'], cell_border['right']['lineColor'])


def draw_rectangle(attributes, line_style, line_width, fore_color, background_color, fill):
    """
    Draw a rectangle on canvas.
    :param attributes:
    :param line_style:
    :param line_width:
    :param fore_color:
    :param background_color:
    :param fill:
    """
    global report

    report['canvas'].saveState()

    report['canvas'].setDash(line_style_dict.get(line_style, (1)))
    report['canvas'].setLineWidth(line_width)
    if fore_color is not None:
        report['canvas'].setStrokeColor(colors.HexColor(fore_color))
    if background_color is not None:
        report['canvas'].setFillColor(colors.HexColor(background_color))
    if attributes.get('radius') is None:
        report['canvas'].rect(attributes['x'],
                              report['cur_y'] - attributes['y'] - attributes['height'],
                              attributes['width'],
                              attributes['height'],
                              fill=fill)
    else:
        report['canvas'].roundRect(attributes['x'],
                                   report['cur_y'] - attributes['y'] - attributes['height'],
                                   attributes['width'],
                                   attributes['height'], radius=attributes.get('radius'),
                                   fill=fill)

    report['canvas'].restoreState()

def process_rectangle(element, row_data):
    """
    Process jrxml "rectangle" element.
    :param element:
    :return:
    """
    global report

    rectangle_element = element.get('child')
    if rectangle_element is not None:
        attributes = process_reportElement(rectangle_element[0].get('reportElement'))  # get reportElement
        # get radius attribute on rectangle element
        add_attr2attributes(element, attributes)

        # set attributes from following graphicElement
        attributes = process_graphicElement(rectangle_element, attributes)

        # set line attributes
        line_style = attributes.get('lineStyle')
        line_width = float(attributes.get('lineWidth', '1.0'))
        fore_color = attributes.get('forecolor')

        mode = attributes.get('mode')
        background_color = attributes.get('backcolor')
        if mode == 'Opaque':
            fill = 1
        else:
            fill = 0

        # draw rectangle
        if line_style == 'Double':  # double line consists of wide solid line with thin white line in between
            draw_rectangle(attributes, line_style_dict['Solid'], line_width*1.0, fore_color, background_color, fill)
            draw_rectangle(attributes, line_style_dict['Solid'], line_width*0.5, '#FFFFFF', background_color, fill)
        else:
            draw_rectangle(attributes, line_style, line_width, fore_color, background_color, fill)


def draw_ellipse(attributes, line_style, line_width, fore_color, background_color, fill):
    """
    Draw an ellipse on canvas.
    :param attributes:
    :param line_style:
    :param line_width:
    :param fore_color:
    :param background_color:
    :param fill:
    :return:
    """
    global report

    report['canvas'].saveState()

    report['canvas'].setDash(line_style_dict.get(line_style, (1)))
    report['canvas'].setLineWidth(line_width)
    if fore_color is not None:
        report['canvas'].setStrokeColor(colors.HexColor(fore_color))
    if background_color is not None:
        report['canvas'].setFillColor(colors.HexColor(background_color))
    # ellipse(cs, cy, rx, ry, stroke=1, fill=0)
    report['canvas'].ellipse(attributes['x'],
                          report['cur_y'] - attributes['y'],
                          attributes['x'] + attributes['width'],
                          report['cur_y'] - attributes['y'] -attributes['height'],
                          fill=fill)
    report['canvas'].restoreState()


def process_ellipse(element, row_data):
    """
    Process jrxml 'ellipse' element.
    :param element:
    """
    global report

    ellipse_element = element.get('child')
    if ellipse_element is not None:
        reportElement = process_reportElement(ellipse_element[0].get('reportElement'))  # get reportElement

        # set attributes from following graphicElement
        reportElement = process_graphicElement(ellipse_element, reportElement)

        # set line attributes
        line_style = reportElement.get('lineStyle')
        line_width = float(reportElement.get('lineWidth', '1.0'))
        fore_color = reportElement.get('forecolor')

        mode = reportElement.get('mode')
        background_color = reportElement.get('backcolor')
        if mode == 'Opaque':
            fill = 1
        else:
            fill = 0

        # draw ellipse
        if line_style == 'Double':  # double line consists of wide solid line with thin white line in between
            draw_ellipse(reportElement, line_style_dict['Solid'], line_width * 1.0, fore_color, background_color,
                         fill)
            draw_ellipse(reportElement, line_style_dict['Solid'], line_width * 0.5, '#FFFFFF', background_color, fill)
        else:
            draw_ellipse(reportElement, line_style, line_width, fore_color, background_color, fill)


def process_image_expression(element, attributes):
    """
    Process jrxml 'image_expression' element.
    :param element: jrxml image_expression element
    :param attributes:
    """
    global report

    image_expression = element.get('value')
    if image_expression is not None:
        image_expression = image_expression.strip('\"')  # strip surrounding quotes

        # image from url
        # logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
        # canvas.drawImage(logo, 10, 10, mask='auto')

        try:
            image = Image.open(image_expression)
            image_width, image_height = image.size

            # drawInlineImage(image, x, y, width=None, height=None, mask=None)
            if attributes.get('scaleImage') == 'Clip':
                im_crop = image.crop((0,0, attributes['width'], attributes['height']))
                report['canvas'].drawInlineImage(im_crop, attributes['x'],
                                                 report['cur_y'] - attributes['y'] - attributes['height'],
                                                 width=attributes['width'], height=attributes['height'])
            elif attributes.get('scaleImage') == 'FillFrame':
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                 report['cur_y'] - attributes['y'] - attributes['height'],
                                                 width=attributes['width'], height=attributes['height'])
            elif attributes.get('scaleImage') == 'RealHeight':
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                     report['cur_y'] - attributes['y'] - hsize)
            elif attributes.get('scaleImage')  == 'RealSize':
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                 report['cur_y'] - attributes['y'] - hsize)
            else:   # reportElement.get('scaleImage') == 'RetainShape': RetainShape is the default behavior
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                vsize = int(image_width * (attributes['height'] / float(image_height)))
                if hsize < vsize:
                    image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                elif hsize > vsize:
                    image = image.resize((vsize, attributes['height']), Image.ANTIALIAS)
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                     report['cur_y'] - attributes['y'] - attributes['height'])
        except FileNotFoundError as err:
            if attributes.get('onErrorType') == 'Blank':
                pass
            elif attributes.get('onErrorType') == 'Icon':
                print('show icon')
            else:
                print(err)

"""
Possible elements under "image" jrxml element.
"""
image_dict = {
    'reportElement': process_reportElement,
    'box': process_box_element,
    'graphicElement': None,
    'imageExpression': process_image_expression
}


def process_image(element, row_data):
    """
    Process jrxml 'image' element.
    :param element: jrxml image element to process
    :param row_data: a row from data source
    """
    # TODO image element may contain $F{} and $V{}. Call replaceText() with row_data
    image_element = element.get('child')
    if image_element is not None:
        reportElement = process_reportElement(image_element[0].get('reportElement'))  # get reportElement
        # get scaleImage attribute on image element
        add_attr2attributes(element, reportElement)
        for tag in image_element[1:]:
            for key, value in tag.items():
                if image_dict[key] is not None:
                    image_dict[key](value, reportElement)


def format_text(text, attributes):
    """
    Format text according to specified pattern.
    :param text: text to format
    :param attributes: attributes corresponding to the text element
    :return: formatted text according to pattern
    """

    if attributes.get('pattern') is not None:
        if type(text) is str:
            pass    # string do not have pattern
        elif type(text) is int:
            if '{:' in attributes['pattern']:
                text = attributes['pattern'].format(int(text))
        elif type(text) is float:
            if '{:' in attributes['pattern']:
                text = attributes['pattern'].format(int(text))
        elif type(text) is complex:
            if '{:' in attributes['pattern']:
                text = attributes['pattern'].format(int(text))
        elif type(text) is bool:
            pass
        elif isinstance(text, datetime.datetime):
            #  check if valid Python pattern. Only execute if invalid Python pattern.
            if '%' in attributes.get('pattern'):
                text = text.strftime(attributes.get('pattern'))
            elif java:
                text = java_formatter.format_date(text, attributes.get('pattern'))
            # try:
            #     text = text.strftime(reportElement.get('pattern'))
            # except:
            #     text = java_formatter(text, reportElement.get('pattern'))

    return text


def convert2boolean(text):
    """
    Convert a string to a boolean type.
    :param text: text to convert to boolean
    :return: 'True' if text is 'true' (case ignored). 'False' otherwise.
    """
    return text is not None and text.lower() == 'true'


def get_font(reportElement, base_style):
    """
    Get specified font name.
    Default to base style font (Usually 'helvetica') if the font is not available in the canvas.
    :param reportElement: jrxml reportElement element
    :param base_style: canvas base style
    :return: valid font name
    """
    global report

    font_name = reportElement.get('fontFontName', base_style.fontName)
    if font_name is not None:
        font_name.strip()
        if font_name not in report['canvas'].getAvailableFonts() and font_name not in report['available_fonts']:
            print('font "' + font_name + '" not found. Replacing with font "' + base_style.fontName + '"')
            font_name = base_style.fontName
    return font_name


def draw_text(text, attributes):
    """
    Draw text string on canvas.
    :param text: text to output to canvas
    :param attributes: attributes (e.g. 'font name', 'font size', 'color') to apply to text
    """
    global report

    text = format_text(text, attributes)
    styles = getSampleStyleSheet()

    text_alignment = {'Left': TA_LEFT, 'Center': TA_CENTER, 'Right': TA_RIGHT, 'Justified': TA_JUSTIFY}
    base_style = styles['Normal']
    left_indent = attributes.get("leftIndent", base_style.leftIndent)
    font_name = get_font(attributes, base_style)

    font_is_bold = convert2boolean(attributes.get('fontIsBold'))
    if font_is_bold:
        text = '<b>' + text + '</b>'
    font_is_italic = convert2boolean(attributes.get('fontIsItalic'))
    if font_is_italic:
        text = '<i>' + text + '</i>'

    font_is_underline = convert2boolean(attributes.get('fontIsUnderline'))
    if font_is_underline:
        text = '<u>' + text + '</u>'
    font_is_strike_through = convert2boolean(attributes.get('fontIsStrikeThrough'))
    if font_is_strike_through:
        text = '<strike>' + text + '</strike>'

    font_size = attributes.get('fontSize', 10)
    text_color = attributes.get('forecolor')
    if text_color is None:
        text_color = base_style.textColor
    else:
        text_color = colors.HexColor(text_color)

    ps = ParagraphStyle(name='cell',
                        parent=styles['Normal'],
                        fontName=font_name,
                        fontSize=font_size,
                        leading=font_size * 1.2,
                        leftIndent=left_indent,
                        alignment=text_alignment[attributes.get('textAlignment', 'Left')],
                        textColor=text_color
                        )

    story = [Paragraph(str(text), ps)]
    story_inframe = KeepInFrame(attributes['width'], attributes['height'], story, mode='shrink')   # 'truncate, overflow, shrink

    data = [[story_inframe]]
    t = Table(data, colWidths=attributes['width'], rowHeights=attributes['height'])

    table_style = TableStyle([
                            ('VALIGN', (0,0),(0,0), attributes.get('verticalAlignment', 'TOP').upper()),
                            ('TEXTCOLOR', (0, 0), (0, 0), colors.black),
                            ('LEFTPADDING', (0, 0), (0, 0), 0),
                            ('RIGHTPADDING', (0, 0), (0, 0), 0),
                            ('TOPPADDING', (0, 0), (0, 0), 0),
                            ('BOTTOMPADDING', (0, 0), (0, 0), 0),
                            ])
    if attributes.get('mode') is not None:
        backcolor = attributes.get('backcolor')
        if backcolor is not None:
            table_style.add('BACKGROUND', (0, 0), (0, 0), colors.HexColor(backcolor))

    t.setStyle(table_style)
    t.wrapOn(report['canvas'], attributes['width'], attributes['height'])
    t.drawOn(report['canvas'], attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'])


def process_text(element, attributes):
    """
    Process "text" jrxml element.
    :param element:
    :param attributes:
    """
    global report
    draw_text(element.get('value',''), attributes)


def add_attr2attributes(element, attributes, prefix=None):
    """
    Add attributes of elements to 'attributes' dictionary.
    :param element:
    :param attributes:
    :param prefix:
    :return:
    """
    attr = element.get('attr')
    if attr is not None:
        for key, value in attr.items():
            if prefix == None:
                dict_key = key
            else:
                dict_key = prefix + key[0].upper() + key[1:]
            if value.isdigit():
                attributes[dict_key] = int(value)
            else:
                attributes[dict_key] = value
    return attributes


def process_font(element, attributes):
    """
    Set font attributes.
    :param element:
    :param reportElement:
    :return:
    """
    return add_attr2attributes(element, attributes, 'font')


def process_paragraph(element, attributes):
    """
    Process paragraph.
    :param element:
    :param attributes:
    :return:
    """
    return add_attr2attributes(element, attributes)


"""Elements within text element."""
text_element_list = {
    'font': process_font,
    'paragraph': process_paragraph
}


def process_textElement(element, attributes):
    """
    textElement is used to specify alignment of the following text
    :param element:
    :param attributes:
    :return:
    """
    text_element = element.get('child')
    if text_element is not None:
        for tag in text_element:
            for key, value in tag.items():
                if text_element_list[key] is not None:
                    attributes = text_element_list[key](value, attributes)

    text_settings = element.get('attr')
    if text_settings is not None:
        for key, value in text_settings.items():
            attributes[key] = value
    return attributes


static_text_dict = {
    'reportElement': process_reportElement,
    'box': process_box_element,
    'textElement': process_textElement,
    'text': process_text
}


def process_static_text(element, row_data):
    """
    Process jrxml staticText element.
    :param element:
    :param row_data: a row from data source
    """
    static_text_element = element.get('child')
    if static_text_element is not None:
        reportElement = process_reportElement(static_text_element[0].get('reportElement'))  # get reportElement
        for tag in static_text_element[1:]:
            for key, value in tag.items():
                if static_text_dict[key] is not None:
                    if key == 'textElement':
                        reportElement = process_textElement(value, reportElement)
                    else:
                        static_text_dict[key](value, reportElement)


def replace_fields(expression, row_data, attributes):
    """
    Replace fields with value from data source.
    If the field is not in the database, do not replace.
    :param expression: text to be processed
    :param row_data: a row from data source
    :param attributes: attribute of the element being processed (i.e. 'isBlankWhenNull')
    :return: expression with $F{} replaced with values from data source when they exist
    """
    if expression is None or row_data is None:
        return None
    else:
        # find all field keys in specified expression
        new_keys = [key[key.find("$F{") + 3:key.find("}")] for key in re.findall('\$F\{.*?\}', expression)]

        if report.get('field_dict') is not None:
            for key in new_keys:
                data_type = report['field_dict'].get(key)
                # TODO need to add more datatype
                if data_type == 'java.lang.Integer':
                    data_value = str(row_data.get(key, '$F{' + key + '}'))
                elif data_type == 'java.sql.Timestamp':
                    date_time = row_data.get(key, '$F{' + key + '}')
                    if type(date_time) is not datetime.datetime:
                        data_value = date_time
                    else:
                        data_value = 'datetime.datetime(' + str(date_time.year) + ',' + str(date_time.month) + ',' \
                                     + str(date_time.day) + ',' + str(date_time.hour) + ',' + str(date_time.minute) + ',' \
                                     + str(date_time.second) + ',' + str(date_time.microsecond) + ',' + str(
                            date_time.tzinfo) + ')'
                else:
                    is_blank_when_null = attributes.get('isBlankWhenNull')
                    value = row_data.get(key, '$F{' + key + '}')
                    if is_blank_when_null and value is None:
                        # data_value = ''
                        return ''
                    else:
                        data_value = '"' + str(row_data.get(key, '$F{' + key + '}')) + '"'
                expression = expression.replace('$F{' + key + '}', data_value)
        return expression
        # try:
        #     return expression
        # except SyntaxError:
        #     return expression


def replace_variables(expression, attributes):
    """
    Replace fields with value from data source.
    If the field is not in the database, do not replace.
    :param expression:
    :param row_data: a row from data source
    :param attributes:
    :return:
    """
    global variables

    # str_expression = str(expression)
    # str_expression = expression
    # find all variable keys in specified expression
    new_keys = [key[key.find("$V{") + 3:key.find("}")] for key in re.findall('\$V\{.*?\}', expression)]

    for key in new_keys:
        var_info = variables.get(key)
        if var_info is None:
            data_value = '$V{' + key + '}'    # do not replace
        else:
            data_type = var_info.get('class')

            # TODO need to add more datatype
            if data_type == 'java.lang.Integer':
                data_value = str(var_info.get('value', '$V{' + key + '}'))
            elif data_type == 'java.sql.Timestamp':
                date_time = var_info.get('value', '$V{' + key + '}')
                if type(date_time) is not datetime.datetime:
                    data_value = date_time
                else:
                    data_value = 'datetime.datetime(' + str(date_time.year) + ',' + str(date_time.month) + ',' \
                                 + str(date_time.day) + ',' + str(date_time.hour) + ',' + str(date_time.minute) + ',' \
                                 + str(date_time.second) + ',' + str(date_time.microsecond) + ',' + str(
                        date_time.tzinfo) + ')'
            else:
                is_blank_when_null = attributes.get('isBlankWhenNull')
                value = var_info.get('value', '$V{' + key + '}')
                if is_blank_when_null and value is None:
                    # data_value = ''
                    return ''
                else:
                    data_value = '"' + str(var_info.get('value', '$V{' + key + '}')) + '"'
        expression = expression.replace('$V{' + key + '}', data_value)
    return expression


def replace_text(expression, row_data, attributes):
    """
    Replace Field and Variables with values ($F{} and $V{}) and evaluate expression.
    :param expression: text element to evaluate
    :param row_data: a row from data source
    :param attributes: attributes of text element to output
    :return: evaluated expression ready for output
    """
    expression = replace_fields(expression, row_data, attributes)   # replace $F{} with values
    expression = replace_variables(expression, attributes)          # replace $V{} with values
    try:
        return eval(expression)
    except SyntaxError:
        return expression
    except NameError:
        return expression


def process_textFieldExpression(element, attributes, row_data):
    """
    Process jrxml textFieldExpression element.
    :param element:
    :param attributes:
    :param row_data: a row from data source
    """
    global report

    data_value = replace_text(element.get('value'), row_data, attributes)
    draw_text(data_value, attributes)


"""
possible child elements under textField element
"""
textField_dict = {
    'reportElement': process_reportElement,
    'box': process_box_element,
    'textElement': process_textElement,
    'textFieldExpression': process_textFieldExpression
}


def process_textField(element, row_data):
    """
    Process textField jrxml element.
    :param element:
    :param row_data: a row from data source
    """
    textField = element.get('child')
    if textField is not None:
        attributes = process_reportElement(textField[0].get('reportElement'))  # get reportElement

        # set attributes to reportElement (e.g. pattern, isBlankWhenNull)
        add_attr2attributes(element, attributes)

        for tag in textField[1:]:
            for key, value in tag.items():
                if textField_dict[key] is not None:
                    if key == 'textElement':
                        attributes = process_textElement(value, attributes)
                    elif key == 'textFieldExpression':
                        textField_dict[key](value, attributes, row_data)
                    else:   # reportElement, box
                        textField_dict[key](value, attributes)


def draw_basic_barcode(type, element, attributes, row_data):
    """
    Draw barcode on canvas.
    :param type: class + method to draw barcode depending of barcode type
    :param element: jrxml element list
    :param attributes: dictionary of attributes to use when drawing an object
    :param row_data: a row from data source
    """
    global report

    codeExpression = element.get('codeExpression')
    if codeExpression is not None:
        data_value = str(replace_text(codeExpression.get('value').strip('\"'), row_data, attributes))
        if attributes.get('checksumRequired', False):
            check_sum = 1
        else:
            check_sum = 0

        report['canvas'].saveState()

        # code127.Code128("text", barHeight= , barWidth=
        barcode = type(data_value, barHeight=attributes.get('barHeight', attributes['height']), stop=1, checksum=check_sum)
        # barcode.drawOn(report['canvas'], reportElement['x'], report['cur_y'] - reportElement['y'] - reportElement.get('barHeight', reportElement['height']))

        # scale barcode to specified width
        report['canvas'].translate(attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'])
        report['canvas'].scale(attributes.get('barWidth', attributes['width'])/barcode.width, attributes.get('barHeight', attributes['height'])/ barcode.height)
        barcode.drawOn(report['canvas'], 0, 0)

        report['canvas'].restoreState()


def draw_advanced_barcode(type, element, attributes, row_data):
    """
    Advanced barcodes are barcodes that requires to be drawn to Drawing objects first.
    Barcodes that drawn to Drawing objects and then put on a canvas.
    :param type:
    :param element:
    :param attributes:
    :param row_data: a row from data source
    """
    global report

    codeExpression = element.get('codeExpression')
    if codeExpression is not None:
        data_value = str(replace_text(codeExpression.get('value').strip('\"'), row_data, attributes))
        barcode = type(data_value)
        bounds = barcode.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        report['canvas'].saveState()
        # Drawing(width, height), transform(a, b, c, d, e, f)
        # d = Drawing(reportElement['width'], reportElement['height'], transform=[45./width,0,0,45./height,0,0])
        d = Drawing(attributes['width'], attributes['height'],
                    transform=[attributes.get('barWidth', attributes['width'])/ width, 0, 0, attributes.get('barHeight', attributes['height']) / height, 0, 0])
        d.add(barcode)
        renderPDF.draw(d, report['canvas'], attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'])

        report['canvas'].restoreState()

"""
Values are (def to used to draw barcode on canvas, barcode component/def)
"""
barcode_types_dict = {
    'Codabar': (draw_basic_barcode, common.Codabar),
    'Code11': (draw_basic_barcode, common.Code11),
    'Code39': (draw_basic_barcode, code39.Standard39),
    'Code39 (Extended)': (draw_basic_barcode, code39.Extended39),
    'Code93': (draw_basic_barcode, code93.Standard93),
    'Code93 (Extended)': (draw_basic_barcode, code93.Extended93),
    'Code128': (draw_basic_barcode, code128.Code128),
    'EAN8': (draw_advanced_barcode, eanbc.Ean8BarcodeWidget),
    'EAN13': (draw_advanced_barcode, eanbc.Ean13BarcodeWidget),
    'EAN128': None,
    'FIM': (draw_basic_barcode, usps.FIM),   # TODO need to check
    'Interleaved2Of5': (draw_basic_barcode, common.I2of5),
    'Int2of5': (draw_basic_barcode, common.I2of5),
    'MSI': (draw_basic_barcode, common.MSI),   # TODO need to check
    'PostNet': (draw_basic_barcode, usps.POSTNET),
    'QRCode': (draw_advanced_barcode, qr.QrCodeWidget),
    'USPS_4State': (draw_basic_barcode, usps4s.USPS_4State),
}

def process_barbecue(key, element, attributes, row_data):
    """
    Process jrxml barbecue component elements.
    :param element: jrxml barbecue element
    :param attributes: attributes of this element
    :param row_data: a row from data source
    """
    add_attr2attributes(element, attributes)
    type = attributes.get('type')
    if type is not None:
        barcode_element_list = element.get('child')
        if barcode_element_list is not None:
            barcode_type = barcode_types_dict.get(type)
            if barcode_type is not None:
                barcode_type[0](barcode_type[1], barcode_element_list[0], attributes, row_data)


def process_barcode4j(key, element, attributes, row_data):
    """
    Process jrxml jarcode4j element.
    :param key:
    :param element:
    :param attributes:
    :param row_data:  a row from data source
    """
    barcode_type = barcode_types_dict.get(key)
    if barcode_type is not None:
        barcode_type[0](barcode_type[1], element.get('child')[0], attributes, row_data)


"""
Supported components.
"""
componentElement_dict = {
    'reportElement': None,
    'barbecue': process_barbecue,
    'Codabar': process_barcode4j,
    'Code11': process_barcode4j,
    'Code128': process_barcode4j,
    'Code39': process_barcode4j,
    'Code39 (Extended)': process_barcode4j,
    'Code93': process_barcode4j,
    'Code93 (Extended)': process_barcode4j,
    'EAN8': process_barcode4j,
    'EAN13': process_barcode4j,
    'EAN128': process_barcode4j,
    'FIM': process_barcode4j,
    'Interleaved2Of5': process_barcode4j,
    'MSI': process_barcode4j,
    'PostNet': process_barcode4j,
    'QRCode': process_barcode4j,
    'USPS_4State': process_barcode4j
}


def process_componentElement(element, row_data):
    """
    Process component jrxml element.
    :param element: jrxml component element
    :param row_data: a row from data source
    """
    component_element = element.get('child')
    if component_element is not None:
        reportElement = process_reportElement(component_element[0].get('reportElement'))  # get reportElement
        for tag in component_element[1:]:
            for key, value in tag.items():
                if componentElement_dict.get(key) is not None:
                    componentElement_dict[key](key, value, reportElement, row_data)

"""Elements in jrxml 'band' element"""
band_elements_dict = {
    'printWhenExpression': None,
    'break': None,
    'line': process_line,
    'rectangle': process_rectangle,
    'ellipse': process_ellipse,
    'image': process_image,
    'staticText': process_static_text,
    'textField': process_textField,
    'frame': None,
    'componentElement': process_componentElement
}


def process_band_element(element):
    """
    Process jrxml band element.
    :param element: jrxml band element
    """
    if element is not None:
        band_element = element.get('child')
        if band_element is not None:
            title_element = band_element[0]
            process_band(title_element.get('band'))


def create_new_page():
    """
    End the current page and create a new page.
    """
    global report, variables

    report['printingFooter'] = True
    column_footer_band()
    page_footer_band()
    report['printingFooter'] = False
    report['canvas'].showPage()
    report['cur_y'] = report['pageHeight'] - report['topMargin']
    page_header_band()
    column_header_band()
    variables['PAGE_NUMBER']['value'] += 1
    variables['PAGE_COUNT']['value'] = 1
    variables['COLUMN_COUNT']['value'] = 1


def process_band(element, row_data=''):
    """
    Process band. Page breaks are inserted when there is not enough space to write a band.
    :param element:
    :param row_data:
    """
    global report   #, page_width, page_height, cur_y, showBoundary

    band_settings = element.get('attr')
    band_height = int(band_settings.get('height', '34'))

     # band_split_type = band_settings.get('splitType', 'Stretch')

    if report['cur_y'] < (report['bottomMargin'] + report['col_footer_height'] + report['page_footer_height']
                          + band_height) and not report['printingFooter']:
        create_new_page()

    if element.get('child') is not None:
        for tag in element.get('child'):
            for key, value in tag.items():
                if band_elements_dict.get(key) is not None:
                    band_elements_dict[key](value, row_data)

    report['cur_y'] = report['cur_y'] - band_height


def process_detail_band_element(element):
    """
    Loop through datasource and output detail band rows
    :param element: 'detail' jrxml element
    """
    global report, variables   #, page_width, page_height, cur_y, showBoundary

    band_element = element.get('child')
    if band_element is not None:
        title_element = band_element[0]

        if report.get('main_datasource') is None:
            row_data = None
            process_band(title_element.get('band'), row_data)
        else:
            # process each data in datasource
            while True:
                if report['main_datasource'] is not None:
                    row = report['main_datasource'].fetch_row()

                    variables['REPORT_COUNT']['value'] += 1
                    variables['PAGE_COUNT']['value'] += 1

                    if row is None:
                        break
                    variables['COLUMN_COUNT']['value'] += 1

                    if type(row) == tuple or type(row) == list:  # regular result set
                        # TODO instead of creating a dictionary, directly use list instead.
                        #  Replace using Field elements entries
                        row_data = dict((field, value) for field, value in zip(report['field_names'], row))
                    elif type(row) == psycopg2.extras.DictRow:  # result in dictionary format
                        row_data = row
                    else:
                        print("invalid datasource format.")
                        row_data = None

                    process_band(title_element.get('band'), row_data)


"""
list of report elements in a report.
"""
report_elements_dict = {
    'property': process_property_band,
    'import': None,
    "template": None,
    "reportFont": None,
    "style": None,
    "subDataset": None,
    "parameter": None,
    "queryString": process_query_string_band,
    "field": process_field_band,
    "sortField": None,
    "variable": process_variable_band,
    "filterExpression": None,
    "group": process_group_band,
    "background": process_background_band,
    "title": process_title_band,
    "pageHeader": page_header_band,
    "columnHeader": column_header_band,
    "detail": process_detail_band_element,
    "columnFooter": column_footer_band,
    "pageFooter": page_footer_band,
    "lastPageFooter": process_band_element,
    'summary': summary_band,
    'noData': process_band_element,
}

"""
Define order to process tags. Tags in jrxml are not in order that they are displayed in a report.
For example, 'Summary' band appears before 'Column Footer' band. 
"""
report_elements_list = [
    'property',
    'import',
    "template",
    "reportFont",
    "style",
    "subDataset",
    "parameter",
    "queryString",
    "field",
    "sortField",
    "variable",
    "filterExpression",
    "group",
    "background",
    "title",
    "pageHeader",
    "columnHeader",
    "detail",
    'summary',
    "columnFooter",
    # "pageFooter",     # pageFooter, lastPageFooter, and noDate are processed separately because they are either one.
    # "lastPageFooter",
    # 'noData'
]


def process_report(root):
    """
    Process main report elements (bands).
    Order and which element to processed is defined in 'report_elements_list'.
    Methods to execute for each element is defined in 'report_elements_dict'.
    :param element:
    """
    global report

    for tag in report_elements_list:    # loop through jrxml elements to be processed
        element = root.get(tag)
        if element is not None:
            for element_tag in element:     # loop through jrxml elements
                for key, value in element_tag.items():
                    if report_elements_dict[key] is not None:   # check if currently supported by AgateReports
                        report_elements_dict[key](value)
    if report.get('lastPageFooter') is not None:    # print lastPageFooter if defined in layout
        report_elements_dict['lastPageFooter'](report['lastPageFooter'][0].get('lastPageFooter'))
    elif report.get('pageFooter') is not None:      # else if pageFooter is defined, print it out
        report_elements_dict['pageFooter'](report['pageFooter'][0].get('pageFooter'))

    # close database cursor/connection
    if report.get('main_datasource') is not None:
        report['main_datasource'].close_cursor()


def process_jasperReport_element(element):
    """
    Get page attributes from the attributes in jrxml 'jasperReport' element.
    Set obtained values to global 'report' variable. Default values are defined here.
    :param element:
    """
    global report
    default_page_width, default_page_height = A4    # set default page size to A4

    page_settings = element.get('attr')

    report['pageWidth'] = float(page_settings.get('pageWidth', default_page_width))
    report['pageHeight'] = float(page_settings.get('pageHeight', default_page_height))
    report['name'] = page_settings.get('name', '')
    report['language'] = page_settings.get('language', 'python')
    report['columnCount'] = float(page_settings.get('columnCount', '1'))
    report['printOrder'] = page_settings.get('printOrder', 'vertical')
    report['orientation'] = page_settings.get('orientation', 'Portrait')
    report['whenNoDataType'] = page_settings.get('whenNoDataType', 'NoPages')
    report['columnWidth'] = float(page_settings.get('columnWidth', '555'))
    report['columnSpacing'] = float(page_settings.get('columnSpacing', '0'))
    report['leftMargin'] = float(page_settings.get('leftMargin', '20'))
    report['rightMargin'] = float(page_settings.get('rightMargin', '20'))
    report['topMargin'] = float(page_settings.get('topMargin', '30'))
    report['bottomMargin'] = float(page_settings.get('bottomMargin', '30'))
    report['isTitleNewPage'] = page_settings.get('isTitleNewPage', 'false')
    report['isSummaryNewPage'] = page_settings.get('isSummaryNewPage', 'false')
    report['isFloatColumnFooter'] = page_settings.get('isFloatColumnFooter', 'false')
    report['scriptletClass'] = page_settings.get('scriptletClass', '')
    report['resourceBundle'] = page_settings.get('resourceBundle', '')
    report['whenResourceMissingType'] = page_settings.get('whenResourceMissingType', 'Null')
    report['isIgnorePagination'] = page_settings.get('isIgnorePagination', 'false')
    report['formatFactoryClass'] = page_settings.get('formatFactoryClass', '')

    # current y axis. To force a new page initially, add +1 to page height
    # report['cur_y'] = report['page_height'] + 1
    report['cur_y'] = report['pageHeight'] - report['topMargin']


def no_pages_process():
    """
    Do nothing here. Saving to file is skipped in generate_pdf() method.
    """
    pass


def blank_page_process():
    """
    Re-initialize canvas and output blank page.
    """
    create_canvas(report['output_filename'])    # clear canvas


def all_sections_no_detail_process():
    """
    Output Title, Page Header, Column Header, Summary, Column Footer, Page Footer.
    Since normal processing will output all these, just pass through.
    """
    pass


def no_data_section_process():
    """
    Re-initialize canvas and output 'No Data' band only.
    """
    global report

    create_canvas(report['output_filename'])    # clear canvas

    report['cur_y'] = report['pageHeight'] - report['topMargin']
    if report.get('noData') is not None:    # print noData band if defined in layout
        report_elements_dict['noData'](report['noData'][0].get('noData'))


"""Dictionary of method to execute when there is no data in datasource."""
when_no_data_type_dict = {
    'NoPages': no_pages_process,
    'NoDataSection': no_data_section_process,
    'BlankPage': blank_page_process,
    'AllSectionsNoDetail': all_sections_no_detail_process,
    'NoDataSection': no_data_section_process,
}


def generate_pdf(input_filename, output_filename, data_source, fonts=None):
    """
    Generate pdf file.
    :param input_filename: name of jrxml file to use.
    :param output_filename: name of output pdf file.
    :param data_source:
    :parm fonts:
    """
    global report

    initialize()    # initialize global variables

    # report['db_settings'] = {'host':  datasource['host'], 'user': datasource['user'],
    #                          'password': datasource['password'], 'database': datasource['database']}
    report['main_datasource'] = data_source

    json = parse_jrxml(input_filename)
    jasper_report_element = json.get('jasperReport')
    process_jasperReport_element(jasper_report_element)

    # create canvas
    create_canvas(output_filename)
    report['output_filename'] = output_filename

    # set fonts if any
    set_fonts(fonts)

    # set band's element to global report[]
    bands = jasper_report_element.get('child')
    for key, value in bands.items():
        report[key] = value

    # set column footer and footer heights. This is used to calculate available height for details band.
    report['col_footer_height'] = calc_column_footer_band_height()
    report['page_footer_height'] = calc_page_footer_band_height()
    report['printingFooter'] = False    # flag to denote if printing out column and page footers

    process_report(bands)

    # if no datasource row was processed and when 'When No Data Type' is <NULL> or 'No Pages',
    # then do not create a report. Otherwise, create a report file.
    if variables['COLUMN_COUNT']['value'] < 1:
        when_no_data_type_dict[report.get('whenNoDataType')]()
        if report.get('whenNoDataType') != 'NoPages':
            write_to_file()
    else:
        write_to_file()     # write canvas to specified file.


def generate_report(input_filename, output_filename, data_source, fonts=None, report_type='pdf'):
    """
    Generate a report.
    :param input_filename: jrxml file to process
    :param output_filename: report file to generate
    :param data_source: database connection dictionary (should contain 'user', 'password', 'host', 'database'. If these
                        keys are not defined, will cause error)
    :param fonts: font list describing fonts used in a report
    :param report_type: output format (currently only pdf is supported.
    """
    if report_type == 'pdf':
        generate_pdf(input_filename, output_filename, data_source, fonts)


if __name__ == '__main__':
    filename = 'group'

    input_filename = '../../tests/jrxml/' + filename + '.jrxml'  # input jrxml filename
    output_filename = '../../tests/output/pdf_' + filename + '.pdf'

    # MySQL datasource
    config = {'host': 'localhost', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    # Postgresql datasource
    # config = "host='172.17.0.2' port='5432' dbname='agatereports' user='python' password='python'"
    # data_source = PostgresqlAdapter(config)

    # CSV datasource
    # csv_filename = '../../tests/data/address.csv'
    # data_source = CSVAdapter(csv_filename)

    fonts = [
        # list of additional directories to search for fonts
        {'font_path': ['../../tests/fonts/', '/usr/share/fonts/truetype/msttcorefonts/']},
        # Japanese font
        {'font_filename': 'ipag.ttc',
         'fonts': [{'index': 0, 'name': 'IPAGothic'},
                   {'index': 1, 'name': 'IPAPGothic'}
                   ]},
        # tests/fonts
        {'font_filename': 'TIMES.TTF',
         'fonts': [{'index': 0, 'name': 'Times_New_Roman'}]},
        {'font_filename': 'TIMESBD.TTF',
         'fonts': [{'index': 1, 'name': 'Times_New_Roman-Bold'}]},
        {'font_filename': 'timesi.ttf',
         'fonts': [{'index': 2, 'name': 'Times_New_Roman-Italic'}]},
        {'font_filename': 'TIMESBI0.TTF',
         'fonts': [{'index': 3, 'name': 'Times_New_Roman-BoldItalic'}]},
        {'font-family':
            {'name': 'Times_New_Roman', 'normal': 'Times_New_Roman', 'bold': 'Times_New_Roman-Bold',
             'italic': 'Times_New_Roman-Italic', 'boldItalic': 'Times_New_Roman-BoldItalic'}
         },
        # tests/fonts. No index
        {'font_filename': 'Vera.ttf',
         'fonts': 'Vera'},
        {'font_filename': 'VeraBd.ttf',
         'fonts': 'Vera-Bold'},
        {'font_filename': 'VeraIt.ttf',
         'fonts': 'Vera-Italic'},
        {'font_filename': 'VeraBI.ttf',
         'fonts': 'Vera-BoldItalic'},
        {'font-family':
            {'name': 'Vera', 'normal': 'Vera', 'bold': 'Vera-Bold', 'italic': 'Vera-Italic',
             'boldItalic': 'Vera-BoldItalic'}
         },
        # ubuntu font
        {'font_filename': 'Verdana.ttf',
         'fonts': [{'index': 0, 'name': 'Verdana'}]},
        {'font_filename': 'Verdana_Bold.ttf',
         'fonts': [{'index': 1, 'name': 'Verdana-Bold'}]},
        {'font_filename': 'Verdana_Italic.ttf',
         'fonts': [{'index': 2, 'name': 'Verdana-Italic'}]},
        {'font_filename': 'Verdana_Bold_Italic.ttf',
         'fonts': [{'index': 3, 'name': 'Verdana-BoldItalic'}]},
        {'font-family':
             {'name': 'Verdana', 'normal': 'Verdana', 'bold': 'Verdana-Bold', 'italic': 'Verdana-Italic',
              'boldItalic': 'Verdana-BoldItalic'}
         }
    ]

    generate_pdf(input_filename, output_filename, data_source, fonts)
