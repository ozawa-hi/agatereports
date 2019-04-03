from reportlab.lib.pagesizes import A4
from agatereports.engine.commonutilities import add_attr2attributes


def process_reportElement(report, element):
    """
    Set attributes of "reportElement" to a dictionary.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    :return: dictionary of attributes of specified element
    """
    text_settings = element.get('attr')
    attributes = {
        'x': int(text_settings.get('x')) + report['leftMargin'],
        'y': int(text_settings.get('y')),
        'height': int(text_settings.get('height', 0)),
        'width': int(text_settings.get('width', 0)),
        'forecolor': text_settings.get('forecolor'),
        'backcolor': text_settings.get('backcolor'),
        'mode': text_settings.get('mode')  # 'Opaque': show
    }
    return attributes


def process_graphicElement(report, element, attributes):
    """
    Process jrxml graphicElement.
    Get attributes on graphicElement.
    :param report: dictionary holding report information
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


def process_jasperReport_element(report, element):
    """
    Get page attributes from the attributes in jrxml 'jasperReport' element.
    Set obtained values to global 'report_info' variable. Default values are defined here.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    default_page_width, default_page_height = A4    # set default page size to A4

    page_settings = element.get('attr')

    report['pageWidth'] = float(page_settings.get('pageWidth', default_page_width))
    report['pageHeight'] = float(page_settings.get('pageHeight', default_page_height))
    report['name'] = page_settings.get('name', '')
    report['language'] = page_settings.get('language', 'python')
    report['columnCount'] = float(page_settings.get('columnCount', '1'))
    report['printOrder'] = page_settings.get('printOrder', 'Vertical')
    report['orientation'] = page_settings.get('orientation', 'Portrait')
    report['whenNoDataType'] = page_settings.get('whenNoDataType', 'Null')
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

