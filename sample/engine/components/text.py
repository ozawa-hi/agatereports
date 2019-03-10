import datetime

from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Table, TableStyle, KeepInFrame
from reportlab.lib import colors


from agatereports.sample.engine.commonutilities import add_attr2attributes, convert2boolean, replace_text
from agatereports.sample.engine.bands.elements import process_reportElement
from agatereports.sample.engine.components.line import process_box_element


def set_fonts(fonts_list):
    """
    Register specified fonts and font families to report_info.
    :param fonts_list: list of fonts and font families to register
    """
    # TODO scan jrxml and try to automatically load fonts

    available_fonts = []
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
                        available_fonts.append(font_list)
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
                                    available_fonts.append(name)
                                except: # if font files is not found, output error and skip it.
                                    print('font not found. font name:' + name + ' file name:' + font_filename)
                            else:
                                try:
                                    pdfmetrics.registerFont(TTFont(name, font_filename))
                                    available_fonts.append(name)
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
    return available_fonts


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
            # elif java:
            #     text = java_formatter.format_date(text, attributes.get('pattern'))
            # try:
            #     text = text.strftime(reportElement.get('pattern'))
            # except:
            #     text = java_formatter(text, reportElement.get('pattern'))
    return text


def process_font(element, attributes):
    """
    Process jrxml 'font' element.
    Set font attributes.
    :param element: jrxml 'font' element
    :param attributes: attributes related to the 'element'
    """
    add_attr2attributes(element, attributes, 'font')


def process_paragraph(element, attributes):
    """
    Process jrxml 'paragraph' element.
    :param element: jrxml 'paragraph' element
    :param attributes: attributes related to the 'element'
    """
    add_attr2attributes(element, attributes)


"""Elements within text element."""
textElement_dict = {
    'font': process_font,
    'paragraph': process_paragraph
}


def process_textElement(report, element, attributes):
    """
    textElement is used to specify alignment of the following text
    :param report: dictionary holding report information
    :param element:
    :param attributes:
    :return:
    """
    textElement = element.get('child')
    if textElement is not None:
        for tag in textElement:
            for key, value in tag.items():
                if textElement_dict[key] is not None:
                    textElement_dict[key](value, attributes)

    text_settings = element.get('attr')
    if text_settings is not None:
        for key, value in text_settings.items():
            attributes[key] = value
    return attributes


def process_text(report, element, attributes):
    """
    Process "text" jrxml element.
    :param report: dictionary holding report information
    :param element:
    :param attributes:
    """
    draw_text(report, element.get('value', ''), attributes)


static_text_dict = {
    # 'reportElement': process_reportElement,
    'box': process_box_element,
    'textElement': process_textElement,
    'text': process_text
}


def process_static_text(report, element):
    """
    Process jrxml staticText element.
    :param report: dictionary holding report information
    :param element:
    :param row_data: a row from data source
    """
    static_text_element = element.get('child')
    if static_text_element is not None:
        report_element = process_reportElement(report, static_text_element[0].get('reportElement'))  # get reportElement
        for tag in static_text_element[1:]:
            for key, value in tag.items():
                if static_text_dict[key] is not None:
                    if key == 'textElement':
                        report_element = process_textElement(report, value, report_element)
                    else:
                        static_text_dict[key](report=report, element=value, attributes=report_element)


def text_element(element):
    # process_text(element)
    pass


def process_textFieldExpression(report, element, attributes):
    """
    Process jrxml textFieldExpression element.
    :param report: dictionary holding report information
    :param element:
    :param attributes:
    """
    data_value = replace_text(report, element.get('value'), attributes)
    draw_text(report, data_value, attributes)


"""
possible child elements under textField element
"""
textField_dict = {
    'reportElement': process_reportElement,
    'box': process_box_element,
    'textElement': process_textElement,
    'textFieldExpression': process_textFieldExpression
}


def process_textField(report, element):
    """
    Process textField jrxml element.
    :param report: dictionary holding report information
    :param element:
    # :param row_data: a row from data source
    """
    text_field = element.get('child')
    if text_field is not None:
        attributes = process_reportElement(report, text_field[0].get('reportElement'))  # get reportElement

        # set attributes to reportElement (e.g. pattern, isBlankWhenNull)
        add_attr2attributes(element, attributes)

        for tag in text_field[1:]:
            for key, value in tag.items():
                if textField_dict[key] is not None:
                    if key == 'textElement':
                        attributes = process_textElement(report, value, attributes)
                    else:   # reportElement, box
                        textField_dict[key](report, value, attributes)


def get_font(report, report_element, base_style):
    """
    Get specified font name.
    Default to base style font (Usually 'helvetica') if the font is not available in the report_info.
    :param report: dictionary holding report information
    :param report_element: jrxml reportElement element
    :param base_style: report_info base style
    :return: valid font name
    """
    font_name = report_element.get('fontFontName', base_style.fontName)
    if font_name is not None:
        font_name.strip()
        if font_name not in report['canvas'].getAvailableFonts() and font_name not in report['available_fonts']:
            print('font file "' + font_name + '" not found. Replacing with font "' + base_style.fontName + '"')
            font_name = base_style.fontName
    return font_name


def draw_text(report, text, attributes):
    """
    Draw text string on report_info.
    :param report:
    :param text: text to output to report_info
    :param attributes: attributes (e.g. 'font name', 'font size', 'color') to apply to text
    """
    report['canvas'].saveState()

    text = format_text(text, attributes)
    styles = getSampleStyleSheet()

    text_alignment = {'Left': TA_LEFT, 'Center': TA_CENTER, 'Right': TA_RIGHT, 'Justified': TA_JUSTIFY}
    base_style = styles['Normal']
    left_indent = attributes.get("leftIndent", base_style.leftIndent)
    right_indent = attributes.get("rightIndent", base_style.leftIndent)
    font_name = get_font(report, attributes, base_style)

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
                        rightIndent=right_indent,
                        alignment=text_alignment[attributes.get('textAlignment', 'Left')],
                        textColor=text_color
                        )

    story = [Paragraph(str(text), ps)]
    story_in_frame = KeepInFrame(attributes['width'], attributes['height'], story, mode='shrink')   # 'truncate, overflow, shrink

    data = [[story_in_frame]]
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

    report['canvas'].restoreState()


def process_text(element, attributes):
    """
    Process "text" jrxml element.
    :param element:
    :param attributes:
    """
    draw_text(element.get('value',''), attributes)
