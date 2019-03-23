from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def when_no_data_blank_page_sample(jrxml_filename = './jrxml/when_no_data_blank_page.jrxml', output_filename = './output/when_no_data_blank_page.pdf' ):
    """
    When no data, blank page sample.

    What to do when datasource is specified but the query return is specified in 'When No Data Type' on a report.
    In this sample, sql query is set to 'SELECT * FROM address WHERE id < 1' to return no result.

    Below are possible values of 'When No Data Type' and description of what will happen.
    Value                       Description
    <NULL>                      no report is generated (no file is created). (default)
    'No Pages'                  same as <NULL>. no report is generated (no file is created).
    'Blank Page'                a blank report is generated.
    'All Sections No Detail'    a report is generated with all bands except 'detail' band.
    'No Data Section'           a report is generated with content of the 'No Data' band.

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    logger.info('running when no data blank page sample')
    # jrxml_filename = './jrxml/when_no_data_blank_page.jrxml'  # input jrxml filename
    # output_filename = './output/when_no_data_blank_page.pdf'  # output pdf filename

    # MySQL datasource
    config = {'adapter': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python',
              'database': 'agatereports'}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    when_no_data_blank_page_sample()
