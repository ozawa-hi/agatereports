import psycopg2
from psycopg2.extras import DictCursor

from agatereports.sample.engine.bands.elements import add_attr2attributes

from agatereports.sample.engine.components.components import process_componentElement
from agatereports.sample.engine.components.image import process_image
from agatereports.sample.engine.components.line import process_line
from agatereports.sample.engine.components.shapes import process_rectangle, process_ellipse
from agatereports.sample.engine.components.text import process_static_text, process_textField
from agatereports.sample.exports.pdf import create_canvas
from agatereports.sample.exports.pdf import write_to_file


def create_new_page(report):
    """
    End the current page and create a new page.
    """
    # global report_info, variables

    report['printingFooter'] = True
    column_footer_band(report)
    page_footer_band(report)
    report['printingFooter'] = False
    report['canvas'].showPage()
    report['cur_y'] = report['pageHeight'] - report['topMargin']
    page_header_band(report)
    column_header_band(report)
    report['variables']['PAGE_NUMBER']['value'] += 1
    report['variables']['PAGE_COUNT']['value'] = 1
    report['variables']['COLUMN_COUNT']['value'] = 1


def process_property_band(report, element):
    """
    Read jrxml properties elements and set to 'properties' dictionary.
    :param report:
    :param properties:
    :param element: jrxml properties element
    """
    # global properties

    # return add_attr2attributes(element, properties)
    add_attr2attributes(element, report.get('properties'))


def process_query_string_band(report, element):
    """
    Read from jrxml queryString element and query a datasource.
    :param element:
    """
    # global report_info

    sql_stmt = element.get('value')
    if sql_stmt is not None:
        sql_stmt = sql_stmt.strip()
        report['field_names'] = report['main_datasource'].execute_query(sql_stmt)


def process_field_band(report, element):
    """
    Process jrxml field element.
    Add field names and it's class (datatype) info to 'field_dict' in global 'report_info' variable.
    :param element:
    :return:
    """
    # global report_info

    field_attr = element.get('attr')
    name = field_attr.get('name')
    datatype = field_attr.get('class')

    if report.get('field_dict') is None:
        report['field_dict'] = dict()
    report['field_dict'][name] = datatype


def process_variable_band(report, element):
    """
    Process jrxml variable element.
    :param element:
    """
    # global variables

    pass    # currently not supported


def process_background_band(report, element):
    """
    Process jrxml background element.
    :param element:
    """
    pass    # currently not supported


def process_group_band(report, element):
    # print(element)
    pass


def process_title_band(report, element=None):
    process_band_element(report, element)


def page_header_band(report, element=None):
    # global report_info

    if element is None:
        page_header =  report.get('pageHeader')
        if page_header is not None:
            element = report['pageHeader'][0]['pageHeader']
    process_band_element(report, element)


def column_header_band(report, element=None):
    # global report_info

    if element is None:
        column_header = report.get('columnHeader')
        if column_header is not None:
            element = report['columnHeader'][0]['columnHeader']
    process_band_element(report, element)


def get_band_height(element):
    return float(element['child'][0]['band']['attr']['height'])


def calc_column_footer_band_height(report):
    # global report_info
    if report.get('columnFooter') is None:
        return 0
    else:
        return get_band_height(report['columnFooter'][0]['columnFooter'])


def column_footer_band(report, element=None):
    # global report_info

    if element is None:
        column_footer = report.get('columnFooter')
        if column_footer is not None:
            element = report['columnFooter'][0]['columnFooter']
    process_band_element(report, element)


def calc_page_footer_band_height(report):
    # global report_info
    if report.get('pageFooter') is None:
        return 0
    else:
        return get_band_height(report['pageFooter'][0]['pageFooter'])


def page_footer_band(report, element=None):
    # global report_info

    if element is None:
        page_footer = report.get('pageFooter')
        if page_footer is not None:
            element = report['pageFooter'][0]['pageFooter']
    process_band_element(report, element)


def summary_band(report, element):
    process_band_element(report, element)



def process_band_element(report, element):
    """
    Process jrxml band element.
    :param element: jrxml band element
    """
    if element is not None:
        band_element = element.get('child')
        if band_element is not None:
            title_element = band_element[0]
            process_band(report, title_element.get('band'))


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


def process_band(report, element, row_data=''):
    """
    Process band. Page breaks are inserted when there is not enough space to write a band.
    :param element:
    :param row_data:
    """
    # global report_info   #, page_width, page_height, cur_y, showBoundary

    band_settings = element.get('attr')
    band_height = int(band_settings.get('height', '34'))

     # band_split_type = band_settings.get('splitType', 'Stretch')

    if report['cur_y'] < (report['bottomMargin'] + report['col_footer_height'] + report['page_footer_height']
                               + band_height) and not report['printingFooter']:
        create_new_page(report)

    if element.get('child') is not None:
        for tag in element.get('child'):
            for key, value in tag.items():
                if band_elements_dict.get(key) is not None:
                    band_elements_dict[key](report=report, element=value, row_data=row_data)

    report['cur_y'] = report['cur_y'] - band_height

def process_detail_band_element(report, element):
    """
    Loop through datasource and output detail band rows
    :param element: 'detail' jrxml element
    """
    # global report_info, variables   #, page_width, page_height, cur_y, showBoundary

    band_element = element.get('child')
    if band_element is not None:
        title_element = band_element[0]

        if report.get('main_datasource') is None:
            row_data = None
            process_band(report, title_element.get('band'), row_data)
        else:
            # process each data in datasource
            while True:
                if report['main_datasource'] is not None:
                    row = report['main_datasource'].fetch_row()

                    report['variables']['REPORT_COUNT']['value'] += 1
                    report['variables']['PAGE_COUNT']['value'] += 1

                    if row is None:
                        break
                    report['variables']['COLUMN_COUNT']['value'] += 1

                    if type(row) == tuple or type(row) == list:  # regular result set
                        # TODO instead of creating a dictionary, directly use list instead.
                        #  Replace using Field elements entries
                        row_data = dict((field, value) for field, value in zip(report['field_names'], row))
                    elif type(row) == psycopg2.extras.DictRow:  # result in dictionary format
                        row_data = row
                    else:
                        print("invalid datasource format.")
                        row_data = None

                    process_band(report, title_element.get('band'), row_data)

"""
list of report_info elements in a report_info.
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
Define order to process tags. Tags in jrxml are not in order that they are displayed in a report_info.
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


def process_no_pages(report_info):
    """
    Do nothing here. Saving to file is skipped in generate_pdf() method.
    """
    pass


def process_blank_page(report):
    """
    Re-initialize report_info and output blank page.
    """
    create_canvas(report, report['output_filename'])    # clear report_info


def process_all_sections_no_detail(report):
    """
    Output Title, Page Header, Column Header, Summary, Column Footer, Page Footer.
    Since normal processing will output all these, just pass through.
    """
    pass


def process_no_data_section(report):
    """
    Re-initialize report_info and output 'No Data' band only.
    """
    # global report_info

    create_canvas(report, report['output_filename'])    # clear report_info

    report['cur_y'] = report['pageHeight'] - report['topMargin']
    if report.get('noData') is not None:    # print noData band if defined in layout
        report_elements_dict['noData'](report, report['noData'][0].get('noData'))


"""Dictionary of method to execute when there is no data in datasource."""
when_no_data_type_dict = {
    'NoPages': process_no_pages,
    'NoDataSection': process_no_data_section,
    'BlankPage': process_blank_page,
    'AllSectionsNoDetail': process_all_sections_no_detail,
    'NoDataSection': process_no_data_section,
}


def process_bands(report, root):
    """
    Process main report_info elements (bands).
    Order and which element to processed is defined in 'report_elements_list'.
    Methods to execute for each element is defined in 'report_elements_dict'.
    :param element:
    """
    # global report_info

    for tag in report_elements_list:    # loop through jrxml elements to be processed
        element = root.get(tag)
        if element is not None:
            for element_tag in element:     # loop through jrxml elements
                for key, value in element_tag.items():
                    if report_elements_dict[key] is not None:   # check if currently supported by AgateReports
                        report_elements_dict[key](report=report, element=value)
    if report.get('lastPageFooter') is not None:    # print lastPageFooter if defined in layout
        report_elements_dict['lastPageFooter'](report, report['lastPageFooter'][0].get('lastPageFooter'))
    elif report.get('pageFooter') is not None:      # else if pageFooter is defined, print it out
        report_elements_dict['pageFooter'](report, report['pageFooter'][0].get('pageFooter'))

    # close database cursor/connection
    if report.get('main_datasource') is not None:
        report['main_datasource'].close_cursor()

    # if no datasource row was processed and when 'When No Data Type' is <NULL> or 'No Pages',
    # then do not create a report_info. Otherwise, create a report_info file.
    if report['variables']['COLUMN_COUNT']['value'] < 1:
        when_no_data_type_dict[report.get('whenNoDataType')](report)
        if report.get('whenNoDataType') != 'NoPages':
            write_to_file(report)
    else:
        write_to_file(report)     # write report_info to specified file.
