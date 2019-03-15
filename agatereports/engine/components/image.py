from PIL import Image
from reportlab.lib.utils import ImageReader
import io
import urllib.request

from agatereports.engine.bands.elements import process_reportElement
from agatereports.engine.commonutilities import add_attr2attributes, replace_text
from agatereports.engine.components.line import process_box_element
from agatereports.engine.constants import protocols, workspace_prefix


import logging
logger = logging.getLogger(__name__)


def align_image(report, attributes, image):
    """
    Calculate x, y of an image based on horizontal alignment, vertical alignment, image size,
    and size specified in the jrxml.
    If the image size is larger, then image size is used.
    If the image size is smaller than the specified size, x and y coordinates are adjusted based on
    specified horizontal alignment and vertical alignment attribute values.
    :param report: dictionary holding report information
    :param attributes: attributes of an image to display
    :param image: image to display
    :return:
    """
    image_width, image_height = image.size
    x = attributes['x']
    if attributes.get('hAlign') == 'Right':
        if attributes['width'] > image_width:
            x += (attributes['width'] - image_width)
    elif attributes.get('hAlign') == 'Center':
        if attributes['width'] > image_width:
            x += (attributes['width'] - image_width) / 2
    y = report['cur_y'] - attributes['y'] - image_height
    if attributes.get('vAlign') == 'Bottom':
        if attributes['height'] > image_height:
            y -= (attributes['height'] - image_height)
    elif attributes.get('vAlign') == 'Middle':
        if attributes['height'] > image_height:
            y -= (attributes['height'] - image_height) / 2
    return [x, y]


def draw_image(report, image, x, y, width, height):
    """
    Draw image on canvas.
    :param report: dictionary holding report information
    :param image: image to draw
    :param x: x coordinate to draw an image
    :param y: y coordinate to draw an image
    :param width: width of a drawn image
    :param height: height of a drawn image
    """
    im_data = io.BytesIO()
    image.save(im_data, format='png')
    im_data.seek(0)
    im_out = ImageReader(im_data)
    report['canvas'].drawImage(im_out, x, y, width=width, height=height, mask='auto')


def process_error(attributes, err):
    """
    Process image error based on 'On Error Type' value.
    :param attributes: attributes corresponding to the image
    :param err: except information
    """
    if attributes.get('onErrorType') == 'Blank':    # do not print any image
        pass
    elif attributes.get('onErrorType') == 'Icon':  # TODO support show icon on error
        logger.debug('show icon')
    else:
        logger.error(err)


def process_image_expression(report, element, attributes):
    """
    Process jrxml 'image_expression' element.
    :param report: dictionary holding report information
    :param element: jrxml image_expression element
    :param attributes:
    """
    image_expression = replace_text(report, element.get('value'), attributes)   # replace fields and variables
    if image_expression is not None:
        report['canvas'].saveState()

        try:
            if isinstance(image_expression, (bytes, memoryview)):
                stream = io.BytesIO(image_expression)
                image = Image.open(stream)
            else:
                image_expression = image_expression.strip('\"')  # strip surrounding quotes
                if image_expression.startswith(protocols):
                    image_file = urllib.request.urlopen(image_expression)
                    image_expression = io.BytesIO(image_file.read())
                elif image_expression.startswith(workspace_prefix):
                    image_expression = image_expression[len(workspace_prefix):]

                image = Image.open(image_expression)
            image_width, image_height = image.size

            # drawInlineImage(image, x, y, width=None, height=None, mask=None)
            if attributes.get('scaleImage') == 'Clip':
                image_width, image_height = image.size
                width = min(image_width, attributes['width'])
                height = min(image_height, attributes['height'])
                im_crop = image.crop((0, 0, width, height))

                x, y = align_image(report, attributes, im_crop)
                # report['canvas'].drawInlineImage(im_crop, x, y, width=width, height=height)
                draw_image(report, im_crop, x, y, width, height)
            elif attributes.get('scaleImage') == 'FillFrame':
                # report['canvas'].drawInlineImage(image, attributes['x'],
                #                                  report['cur_y'] - attributes['y'] - attributes['height'],
                #                                  width=attributes['width'], height=attributes['height'])
                draw_image(report, image, attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'],
                           width=attributes['width'], height=attributes['height'])
            elif attributes.get('scaleImage') == 'RealHeight':
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                # report['canvas'].drawInlineImage(image, attributes['x'],
                #                                  report['cur_y'] - attributes['y'] - hsize)
                width, height = image.size
                draw_image(report, image, attributes['x'], report['cur_y'] - attributes['y'] - hsize,
                           width, height)

            elif attributes.get('scaleImage') == 'RealSize':
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                # report['canvas'].drawInlineImage(image, attributes['x'],
                #                                  report['cur_y'] - attributes['y'] - hsize)
                width, height = image.size
                draw_image(report, image, attributes['x'], report['cur_y'] - attributes['y'] - hsize,
                           width, height)
            else:   # reportElement.get('scaleImage') == 'RetainShape': RetainShape is the default behavior
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                vsize = int(image_width * (attributes['height'] / float(image_height)))
                if hsize < vsize:
                    image_resize = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                elif hsize > vsize:
                    image_resize = image.resize((vsize, attributes['height']), Image.ANTIALIAS)
                else:
                    image_resize = image.resize((hsize, vsize), Image.ANTIALIAS)  # Image.LANCZOS
                x, y = align_image(report, attributes, image_resize)
                # report['canvas'].drawInlineImage(image, x, y)
                width, height = image_resize.size
                draw_image(report, image_resize, x, y, width, height)

        except FileNotFoundError as err:
            # if attributes.get('onErrorType') == 'Blank':
            #     pass
            # elif attributes.get('onErrorType') == 'Icon':   # TODO support show icon on error
            #     logger.debug('show icon')
            # else:
            #     logger.error(err)
            process_error(attributes, err)
        except urllib.request.URLError as err:
            process_error(attributes, err)
        report['canvas'].restoreState()


"""
Possible elements under "image" jrxml element.
"""
image_dict = {
    'reportElement': process_reportElement,
    'box': process_box_element,
    'graphicElement': None,
    'imageExpression': process_image_expression
}


def process_image(report, element):
    """
    Process jrxml 'image' element.
    :param report: dictionary holding report information
    :param element: jrxml image element to process
    """
    image_element = element.get('child')
    if image_element is not None:
        report_element = process_reportElement(report, image_element[0].get('reportElement'))  # get reportElement
        # get scaleImage attribute on image element
        add_attr2attributes(element, report_element)
        for tag in image_element[1:]:
            for key, value in tag.items():
                if image_dict[key] is not None:
                    image_dict[key](report, value, report_element)
