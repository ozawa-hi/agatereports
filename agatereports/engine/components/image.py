from PIL import Image

from agatereports.engine.bands.elements import add_attr2attributes, process_reportElement
from agatereports.engine.components.line import process_box_element

import logging
logger = logging.getLogger(__name__)


def align_image(report, attributes, image):
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


def process_image_expression(report, element, attributes):
    """
    Process jrxml 'image_expression' element.
    :param report: dictionary holding report information
    :param element: jrxml image_expression element
    :param attributes:
    """
    image_expression = element.get('value')
    if image_expression is not None:
        image_expression = image_expression.strip('\"')  # strip surrounding quotes

        report['canvas'].saveState()

        # image from url
        # logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
        # report_info.drawImage(logo, 10, 10, mask='auto')

        try:
            image = Image.open(image_expression)
            image_width, image_height = image.size

            # drawInlineImage(image, x, y, width=None, height=None, mask=None)
            if attributes.get('scaleImage') == 'Clip':
                image_width, image_height = image.size
                width = min(image_width, attributes['width'])
                height = min(image_height, attributes['height'])
                im_crop = image.crop((0, 0, width, height))
                x, y = align_image(report, attributes, im_crop)
                report['canvas'].drawInlineImage(im_crop, x, y, width=width, height=height)
            elif attributes.get('scaleImage') == 'FillFrame':
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                 report['cur_y'] - attributes['y'] - attributes['height'],
                                                 width=attributes['width'], height=attributes['height'])
            elif attributes.get('scaleImage') == 'RealHeight':
                hsize = int(image_height * (attributes['width'] / float(image_width)))
                image = image.resize((attributes['width'], hsize), Image.ANTIALIAS)
                report['canvas'].drawInlineImage(image, attributes['x'],
                                                 report['cur_y'] - attributes['y'] - hsize)
            elif attributes.get('scaleImage') == 'RealSize':
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

                x, y = align_image(report, attributes, image)
                report['canvas'].drawInlineImage(image, x, y)

        except FileNotFoundError as err:
            if attributes.get('onErrorType') == 'Blank':
                pass
            elif attributes.get('onErrorType') == 'Icon':   # TODO support show icon on error
                logger.debug('show icon')
            else:
                logger.error(err)
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
    # TODO image element may contain $F{} and $V{}. Call replaceText() with row_data
    image_element = element.get('child')
    if image_element is not None:
        report_element = process_reportElement(report, image_element[0].get('reportElement'))  # get reportElement
        # get scaleImage attribute on image element
        add_attr2attributes(element, report_element)
        for tag in image_element[1:]:
            for key, value in tag.items():
                if image_dict[key] is not None:
                    image_dict[key](report, value, report_element)
