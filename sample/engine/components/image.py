from PIL import Image

from agatereports.sample.engine.bands.elements import add_attr2attributes, process_reportElement
from agatereports.sample.engine.components.line import process_box_element


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

        # image from url
        # logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
        # report_info.drawImage(logo, 10, 10, mask='auto')

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
