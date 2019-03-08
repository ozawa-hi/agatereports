from reportlab.lib.pagesizes import A4
from agatereports.sample.engine.commonutilities import add_attr2attributes


def process_reportElement(report, element):
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


def process_graphicElement(report, element, attributes):
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


def process_jasperReport_element(report_info, element):
    """
    Get page attributes from the attributes in jrxml 'jasperReport' element.
    Set obtained values to global 'report_info' variable. Default values are defined here.
    :param element:
    """
    # global report_info
    default_page_width, default_page_height = A4    # set default page size to A4

    page_settings = element.get('attr')

    report_info['pageWidth'] = float(page_settings.get('pageWidth', default_page_width))
    report_info['pageHeight'] = float(page_settings.get('pageHeight', default_page_height))
    report_info['name'] = page_settings.get('name', '')
    report_info['language'] = page_settings.get('language', 'python')
    report_info['columnCount'] = float(page_settings.get('columnCount', '1'))
    report_info['printOrder'] = page_settings.get('printOrder', 'vertical')
    report_info['orientation'] = page_settings.get('orientation', 'Portrait')
    report_info['whenNoDataType'] = page_settings.get('whenNoDataType', 'NoPages')
    report_info['columnWidth'] = float(page_settings.get('columnWidth', '555'))
    report_info['columnSpacing'] = float(page_settings.get('columnSpacing', '0'))
    report_info['leftMargin'] = float(page_settings.get('leftMargin', '20'))
    report_info['rightMargin'] = float(page_settings.get('rightMargin', '20'))
    report_info['topMargin'] = float(page_settings.get('topMargin', '30'))
    report_info['bottomMargin'] = float(page_settings.get('bottomMargin', '30'))
    report_info['isTitleNewPage'] = page_settings.get('isTitleNewPage', 'false')
    report_info['isSummaryNewPage'] = page_settings.get('isSummaryNewPage', 'false')
    report_info['isFloatColumnFooter'] = page_settings.get('isFloatColumnFooter', 'false')
    report_info['scriptletClass'] = page_settings.get('scriptletClass', '')
    report_info['resourceBundle'] = page_settings.get('resourceBundle', '')
    report_info['whenResourceMissingType'] = page_settings.get('whenResourceMissingType', 'Null')
    report_info['isIgnorePagination'] = page_settings.get('isIgnorePagination', 'false')
    report_info['formatFactoryClass'] = page_settings.get('formatFactoryClass', '')

    # current y axis. To force a new page initially, add +1 to page height
    # report_info['cur_y'] = report_info['page_height'] + 1
    report_info['cur_y'] = report_info['pageHeight'] - report_info['topMargin']

