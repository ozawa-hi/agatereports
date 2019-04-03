import psycopg2
from psycopg2.extras import DictCursor

from agatereports.engine.bands.elements import add_attr2attributes

from agatereports.engine.components.components import process_componentElement
from agatereports.engine.components.image import process_image
from agatereports.engine.components.line import process_line
from agatereports.engine.components.shapes import process_rectangle, process_ellipse, process_circle
from agatereports.engine.components.text import process_static_text, process_textField
from agatereports.exports.pdf import create_canvas, write_to_file

import logging
logger = logging.getLogger(__name__)


# check jasperreports.xsd file in jasperreport library source on information about jrxml elements construct.

def create_new_page(report):
    """
    End the current page and create a new page.
    :param report: dictionary holding report information
    """
    report['printingFooter'] = True
    column_footer_band(report)
    page_footer_band(report)
    report['printingFooter'] = False
    report['canvas'].showPage()
    report['cur_y'] = report['pageHeight'] - report['topMargin']
    page_header_band(report=report, force=True)
    column_header_band(report=report, force=True)
    report['variables']['PAGE_NUMBER']['value'] += 1
    report['variables']['PAGE_COUNT']['value'] = 1
    report['variables']['COLUMN_COUNT']['value'] = 1


def process_property_band(report, element):
    """
    Read jrxml properties elements and set to 'properties' dictionary.
    :param report: dictionary holding report information
    :param properties:
    :param element: jrxml properties element
    """
    # return add_attr2attributes(element, properties)
    add_attr2attributes(element, report.get('properties'))


def process_query_string_band(report, element):
    """
    Read from jrxml queryString element and query a datasource.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    sql_stmt = element.get('value')
    if sql_stmt is None:
        report['main_datasource'] = None
    else:
        sql_stmt = sql_stmt.strip()
        # TODO instead of getting field names from query, get from 'field' element list
        report['main_datasource'].execute_query(sql_stmt)
        # instead of getting field names from datasourvce, get field names field elements
        # report['field_names'] = report['main_datasource'].execute_query(sql_stmt)


def process_field_band(report, element):
    """
    Process jrxml field element.
    Add field names and it's class (datatype) info to 'field_dict' in global 'report_info' variable.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    field_attr = element.get('attr')
    name = field_attr.get('name')
    datatype = field_attr.get('class')

    if report.get('field_dict') is None:
        report['field_dict'] = dict()
    report['field_dict'][name] = datatype

    if report.get('field_names') is None:
        report['field_names'] = [name]
    else:
        report['field_names'].append(name)
    # print(report['field_names'])


def process_variable_band(report, element):
    """
    Process jrxml variable element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    pass    # currently not supported


def process_background_band(report, element):
    """
    Process jrxml background element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    pass    # currently not supported


def process_groupExpression(report, element):
    """
    Process groupExpression element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    :return:
    """
    if element is not None:
        # group_name = report['group_cur'][-1]
        report['group_names'].update({report['group_cur'][-1]: element.get('value')})


def process_groupHeader(report, element):
    """
    Process group header element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    if element is not None:
        if report.get('main_datasource') is None:  # when there is no datasource, just process static page
            # row_data = None
            check_for_new_page(report)

            process_band_element(report, element)
        else:
            check_for_new_page(report)
            report_elements_list.remove('detail')   # call details from below while loop
            while True:
                row = report['main_datasource'].fetch_row()
                if row is None:     # there is no data in datasource then just print content in jrxml layout
                    if not report['output_to_canvas']:
                        check_for_new_page(report)
                        process_band_element(report, element)
                        report['output_to_canvas'] = True
                    break
                elif report['group_names'].get(report['group_cur'][-1]) is None:
                    # print('no expression', report.get('group_names'))
                    check_for_new_page(report)
                    process_datasource_row(row, report)
                    process_band_element(report, element)
                    report['output_to_canvas'] = True

                    detail_band = report.get('detail')
                    if detail_band is not None and len(detail_band) > 0:
                        detail = detail_band[0].get('detail')
                        detail_band_child = detail.get('child')
                        if detail_band_child is not None:
                            detail_element = detail_band_child[0]
                            # loop through detail band
                            while row is not None:
                                process_band(report, detail_element.get('band'))
                                row = fetch_from_datasource(report)
                    break
                else:   # if there is some row in datasource
                    check_for_new_page(report)
                    process_datasource_row(row, report)
                    # check if there is a prev value or if there is current group
                    if not report['prev_value'] or report['group_cur'] is None:
                        process_band_element(report, element)
                        report['prev_value'] = report['row_data']
                        report['output_to_canvas'] = True
                    else:
                        cur_group_value = report['row_data'].get(report['group_cur'][-1])
                        if report['prev_value'].get(report['group_cur'][-1]) != cur_group_value:
                            process_band_element(report, element)
                            report['prev_value'] = report['row_data']
                            report['output_to_canvas'] = True


def process_groupFooter(report, element):
    """
    Process groupFooter element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    if element is not None:
        if report.get('canvas') is None:
            create_canvas(report)
        process_band_element(report, element)


"""supported jrxml elements under group element"""
group_element_dict={
    'groupExpression': process_groupExpression,
    'groupHeader': process_groupHeader,
    'groupFooter': process_groupFooter
}


def process_group_band(report, element):
    """
    Process group element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    group_attr = element.get('attr')
    report['group_names'].update({group_attr.get('name'): None})
    report['group_cur'].append(group_attr.get('name'))
    # report['group_cur'] = group_attr.get('name')

    if element.get('child') is not None:
        for tag in element.get('child'):
            for key, value in tag.items():
                if group_element_dict.get(key) is not None:
                    group_element_dict[key](report, value)
    report['group_cur'].pop()


    # if report.get('main_datasource') is None:  # when there is no datasource, just process static page
    #     row_data = None
    #     check_for_new_page(report)
    #
    #
    #
    # else:
    #     check_for_new_page(report)
    #
    #
    #     # if there is a field in group's textFieldExpression then loop else just process
    #     while True:
    #
    #         row = report['main_datasource'].fetch_row()
    #
    #         report['variables']['REPORT_COUNT']['value'] += 1
    #         report['variables']['PAGE_COUNT']['value'] += 1
    #
    #         if row is None:
    #             break
    #         report['variables']['COLUMN_COUNT']['value'] += 1
    #
    #         if element.get('child') is not None:
    #             for tag in element.get('child'):
    #                 for key, value in tag.items():
    #                     if group_element_dict.get(key) is not None:
    #                         group_element_dict[key](report, value)
    #
    # report['output_to_canvas'] = True   # TODO this needs to be moved to code actually writing to canvas


def process_title_band(report, element=None):
    """
    Process title element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    if not report['output_to_canvas']:
        if report.get('canvas') is None:
            create_canvas(report)
        process_band_element(report, element)


def page_header_band(report, element=None, force=False):
    """
    Process pageHeader element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    :param force: True if unconditionally output, False if only output if nothing is yet output to canvas
    """
    if not report['output_to_canvas'] or force:
        if element is None:
            page_header = report.get('pageHeader')
            if page_header is not None:
                element = report['pageHeader'][0]['pageHeader']

        if report.get('canvas') is None:
            create_canvas(report)
        process_band_element(report, element)


def column_header_band(report, element=None, force=False):
    """
    Process columnHeader element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    :param force: True if unconditionally output, False if only output if nothing is yet output to canvas
    """
    if not report['output_to_canvas'] or force:
        if element is None:
            column_header = report.get('columnHeader')
            if column_header is not None:
                element = report['columnHeader'][0]['columnHeader']
        if report.get('canvas') is None:
            create_canvas(report)
        process_band_element(report, element)


def get_band_height(element):
    """
    Return height the the specified element.
    :param element: current jrxml element being processes.
    :return:
    """
    return float(element['child'][0]['band']['attr']['height'])


def calc_column_footer_band_height(report):
    """
    Calculate column footer band height.
    :param report: dictionary holding report information
    :return: height of column footer band.
    """
    if report.get('columnFooter') is None:
        return 0
    else:
        return get_band_height(report['columnFooter'][0]['columnFooter'])


def column_footer_band(report, element=None):
    """
    Process columnFooter element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    :return:
    """
    if element is None:
        column_footer = report.get('columnFooter')
        if column_footer is not None:
            element = report['columnFooter'][0]['columnFooter']
    if report.get('canvas') is None:
        create_canvas(report)
    report['printingFooter'] = True
    process_band_element(report, element)


def calc_page_footer_band_height(report):
    """
    Calculate pageFooter band height.
    :param report: dictionary holding report information
    :return: page footer band height
    """
    if report.get('pageFooter') is None:
        return 0
    else:
        return get_band_height(report['pageFooter'][0]['pageFooter'])


def page_footer_band(report, element=None):
    """
    Process jrxml 'pageFooter' element.
    :param report: dictionary holding report information
    :param element: parent element of jrxml 'pageFooter' element
    """
    if element is None:
        page_footer = report.get('pageFooter')
        if page_footer is not None:
            element = report['pageFooter'][0]['pageFooter']
    if report.get('canvas') is None:
        create_canvas(report)
    report['printingFooter'] = True
    process_band_element(report, element)


def summary_band(report, element):
    """
    Process jrxml 'summmary' element.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
    if report.get('canvas') is None:
        create_canvas(report)
    report['printingFooter'] = True
    process_band_element(report, element)


def process_band_element(report, element):
    """
    Process jrxml band element.
    :param report: dictionary holding report information
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
    'circle': process_circle,
    'image': process_image,
    'staticText': process_static_text,
    'textField': process_textField,
    'frame': None,
    'componentElement': process_componentElement
}


def process_band(report, element):
    """
    Process jrxml band element. Page breaks are inserted when there is not enough space to write a band.
    :param report: dictionary holding report information
    :param element: current jrxml element being processes.
    """
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
                    # band_elements_dict[key](report=report, element=value, row_data=row_data)
                    band_elements_dict[key](report=report, element=value)

    report['cur_y'] = report['cur_y'] - band_height


# def fetch_row_data(report, element, row):
#     """
#     Loop through datasource and output detail band rows
#     :param element: 'detail' jrxml element
#     """
#
#             while True:
#                 if report['main_datasource'] is not None:
#                     row = report['main_datasource'].fetch_row()
#
#                     report['variables']['REPORT_COUNT']['value'] += 1
#                     report['variables']['PAGE_COUNT']['value'] += 1
#
#                     if row is None:
#                         break
#                     report['variables']['COLUMN_COUNT']['value'] += 1
#
#                     if type(row) == tuple or type(row) == list:  # regular result set
#                         # TODO instead of creating a dictionary, directly use list instead.
#                         #  Replace using Field elements entries
#                         row_data = dict((field, value) for field, value in zip(report['field_names'], row))
#                     elif type(row) == psycopg2.extras.DictRow:  # result in dictionary format
#                         row_data = row
#                     else:
#                         logger.error("invalid datasource format.")
#                         row_data = None
#
#                     process_band(report, title_element.get('band'), row_data)


def check_for_new_page(report):
    if report.get('canvas') is None:
        create_canvas(report)
        if report.get('title') is not None:
            report_elements_dict['title'](report, report['title'][0].get('title'))
        if report.get('pageHeader') is not None:
            report_elements_dict['pageHeader'](report, report['pageHeader'][0].get('pageHeader'))
        if report.get('columnHeader') is not None:
            report_elements_dict['columnHeader'](report, report['columnHeader'][0].get('columnHeader'))


def process_datasource_row(row, report):
    if type(row) == tuple or type(row) == list:  # regular result set
        # TODO instead of creating a dictionary, directly use list instead.
        #  Replace using Field elements entries
        report['row_data'] = dict((field, value) for field, value in zip(report['field_names'], row))
    elif type(row) == psycopg2.extras.DictRow:  # result in dictionary format
        report['row_data'] = row
    else:
        logging.error("invalid datasource format.")
        report['row_data'] = None


def fetch_from_datasource(report):
    row = report['main_datasource'].fetch_row()

    report['variables']['REPORT_COUNT']['value'] += 1
    report['variables']['PAGE_COUNT']['value'] += 1

    # if row is None:
    #     break
    if row is not None:
        report['variables']['COLUMN_COUNT']['value'] += 1
        process_datasource_row(row, report)
    return row


def process_detail_band_element(report, element):
    """
    Loop through datasource and output detail band rows
    :param report: dictionary holding report information
    :param element: 'detail' jrxml element
    """

    band_element = element.get('child')
    if band_element is not None:    # only process if there is a jrxml 'band' element
        detail_element = band_element[0]

        # check_for_new_page(report)

        if report.get('main_datasource') is None:   # when there is no datasource, just process static page
            row_data = None
            check_for_new_page(report)

            # process_band(report, title_element.get('band'), row_data)

            process_band(report, detail_element.get('band'))
        else:
            # fetch row from datasource and process each row
            check_for_new_page(report)
            row = fetch_from_datasource(report)
            while row is not None:
                # if fetch_from_datasource(report) is None:
                #     break;
                # if report['main_datasource'] is not None:
                # row = report['main_datasource'].fetch_row()
                #
                # report['variables']['REPORT_COUNT']['value'] += 1
                # report['variables']['PAGE_COUNT']['value'] += 1
                #
                # if row is None:
                #     break
                # report['variables']['COLUMN_COUNT']['value'] += 1
                #
                # process_datasource_row(row, report)
                process_band(report, detail_element.get('band'))
                row = fetch_from_datasource(report)
                # TODO if page per record, then set report['canvas'] = None

                # if type(row) == tuple or type(row) == list:  # regular result set
                #     # TODO instead of creating a dictionary, directly use list instead.
                #     #  Replace using Field elements entries
                #     report['row_data'] = dict((field, value) for field, value in zip(report['field_names'], row))
                # elif type(row) == psycopg2.extras.DictRow:  # result in dictionary format
                #     report['row_data'] = row
                # else:
                #     logging.error("invalid datasource format.")
                #     report['row_data'] = None
                # process_band(report, detail_element.get('band'))
                # # TODO if page per record, then set report['canvas'] = None
    report['output_to_canvas'] = True   # TODO this needs to be moved to code actually writing to canvas


def process_last_page_footer(report, element):
    if report.get('canvas') is None:
        create_canvas(report)
    report['printingFooter'] = True
    process_band_element(report, element)


def process_no_data(report, element):
    if report.get('canvas') is None:
        create_canvas(report)
    report['printingFooter'] = True
    process_band_element(report, element)


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
    "lastPageFooter": process_last_page_footer,
    'summary': summary_band,
    'noData': process_no_data,
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
    "background",
    # "title",          # process title, pageHeader, columnHeader after later to make it possible to have
    # "pageHeader",     # filename based on datasource
    # "columnHeader",
    "group",          # TODO currently not supported. Need to read datasource in group
    "detail",
    'summary',
    "columnFooter",
    "title",
    "pageHeader",
    "columnHeader",
    # "group",
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
    :param report: dictionary holding report information
    """
    # create_canvas(report, report['output_filename'])    # clear report_info
    create_canvas(report)  # clear report_info


def process_all_sections_no_detail(report):
    """
    Output Title, Page Header, Column Header, Summary, Column Footer, Page Footer.
    Since normal processing will output all these, just pass through.
    :param report: dictionary holding report information
    """
    pass


def process_no_data_section(report):
    """
    Re-initialize report_info and output 'No Data' band only.
    :param report: dictionary holding report information
    """
    # create_canvas(report, report['output_filename'])    # clear report_info
    create_canvas(report)  # clear report_info

    report['cur_y'] = report['pageHeight'] - report['topMargin']
    if report.get('noData') is not None:    # print noData band if defined in layout
        report_elements_dict['noData'](report, report['noData'][0].get('noData'))


def process_null_data(report):
    pass


"""Dictionary of method to execute when there is no data in datasource."""
when_no_data_type_dict = {
    'Null': process_null_data,
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
    :param report: dictionary holding report information
    :param root: jrxml 'jasperReport' element
    """
    for tag in report_elements_list:    # loop through jrxml elements to be processed
        element = root.get(tag)
        if element is not None:
            for element_tag in element:     # loop through jrxml elements
                for key, value in element_tag.items():
                    if report_elements_dict[key] is not None:   # process only if currently supported by AgateReports
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
    if report['main_datasource'] is not None and report['variables']['COLUMN_COUNT']['value'] < 1:
        when_no_data_type_dict[report.get('whenNoDataType')](report)
        if report.get('whenNoDataType') != 'NoPages':
            write_to_file(report)
    else:
        write_to_file(report)     # write report_info to specified file.
