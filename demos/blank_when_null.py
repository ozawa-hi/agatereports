from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def blank_when_null_sample(jrxml_filename = './jrxml/blank_when_null.jrxml', output_filename = './output/blank_when_null.pdf'):
    """
    Blank when null sample.
    When 'Blank When NULL' is checked on a TextField properties, no value will be displayed when the value is None.
    Otherwise, string 'None' will be displayed.

    In this sample, columns 'street' and column 'city' in the first row is None.
    Also, in the report layout, column 'street' is NOT set to 'Blank when Null' while column 'city' is set.
    As such, 'None' is displayed in column 'street' in the first row while column 'city' is blank in the first row.

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    logger.info('running blank when null sample')
    # jrxml_filename = './jrxml/blank_when_null.jrxml'  # input jrxml filename
    # output_filename = './output/blank_when_null.pdf'  # output pdf filename

    # MySQL datasource
    config = {'adapter': 'mysql', 'host': 'localhost', 'port': '3306','user': 'python', 'password': 'python',
               'database': 'agatereports'}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    blank_when_null_sample()
