from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps, usps4s, common
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from agatereports.sample.engine.commonutilities import replace_text, add_attr2attributes


def draw_basic_barcode(report, type, element, attributes, row_data):
    """
    Draw barcode on report_info.
    :param report_info: dictionary containing output information
    :param type: class + method to draw barcode depending of barcode type
    :param element: jrxml element list
    :param attributes: dictionary of attributes to use when drawing an object
    :param row_data: a row from data source
    """
    # global report_info

    code_expression = element.get('codeExpression')
    if code_expression is not None:
        data_value = str(replace_text(report, code_expression.get('value').strip('\"'), row_data, attributes))
        if attributes.get('checksumRequired', False):
            check_sum = 1
        else:
            check_sum = 0

        report['canvas'].saveState()

        barcode = type(data_value, barHeight=attributes.get('barHeight', attributes['height']), stop=1, checksum=check_sum)
        # barcode.drawOn(report_info['report_info'], reportElement['x'], report_info['cur_y'] - reportElement['y'] - reportElement.get('barHeight', reportElement['height']))

        # scale barcode to specified width
        report['canvas'].translate(attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'])
        report['canvas'].scale(attributes.get('barWidth', attributes['width'])/barcode.width,
                             attributes.get('barHeight', attributes['height'])/ barcode.height)
        barcode.drawOn(report['canvas'], 0, 0)

        report['canvas'].restoreState()


def draw_advanced_barcode(report, type, element, attributes, row_data):
    """
    Advanced barcodes are barcodes that requires to be drawn to Drawing objects first.
    Barcodes that drawn to Drawing objects and then put on a report_info.
    :param type:
    :param element:
    :param attributes:
    :param row_data: a row from data source
    """
    # global report_info

    code_expression = element.get('codeExpression')
    if code_expression is not None:
        data_value = str(replace_text(report, code_expression.get('value').strip('\"'), row_data, attributes))
        barcode = type(data_value)
        bounds = barcode.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        report['canvas'].saveState()
        # Drawing(width, height), transform(a, b, c, d, e, f)
        # d = Drawing(reportElement['width'], reportElement['height'], transform=[45./width,0,0,45./height,0,0])
        d = Drawing(attributes['width'], attributes['height'],
                    transform=[attributes.get('barWidth', attributes['width'])/ width, 0, 0,
                               attributes.get('barHeight', attributes['height']) / height, 0, 0])
        d.add(barcode)
        renderPDF.draw(d, report['canvas'], attributes['x'], report['cur_y'] - attributes['y'] - attributes['height'])

        report['canvas'].restoreState()


"""
Values are (def to used to draw barcode on report_info, barcode component/def)
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


def process_barbecue(report, key, element, attributes, row_data):
    """
    Process jrxml barbecue component elements.
    :param element: jrxml barbecue element
    :param attributes: attributes of this element
    :param row_data: a row from data source
    """
    # attributes = add_attr2attributes(element, attributes)
    add_attr2attributes(element, attributes)
    type = attributes.get('type')
    if type is not None:
        barcode_element_list = element.get('child')
        if barcode_element_list is not None:
            barcode_type = barcode_types_dict.get(type)
            if barcode_type is not None:
                barcode_type[0](report, barcode_type[1], barcode_element_list[0], attributes, row_data)


def process_barcode4j(report, key, element, attributes, row_data):
    """
    Process jrxml jarcode4j element.
    :param key:
    :param element:
    :param attributes:
    :param row_data:  a row from data source
    """
    barcode_type = barcode_types_dict.get(key)
    if barcode_type is not None:
        barcode_type[0](report, barcode_type[1], element.get('child')[0], attributes, row_data)


