from agatereports.sample.engine.components.barcode import process_barbecue, process_barcode4j
from agatereports.sample.engine.bands.elements import process_reportElement

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


def process_componentElement(report, element, row_data):
    """
    Process component jrxml element.
    :param element: jrxml component element
    :param row_data: a row from data source
    """
    component_element = element.get('child')
    if component_element is not None:
        reportElement = process_reportElement(report, component_element[0].get('reportElement'))  # get reportElement
        for tag in component_element[1:]:
            for key, value in tag.items():
                if componentElement_dict.get(key) is not None:
                    componentElement_dict[key](report, key, value, reportElement, row_data)
