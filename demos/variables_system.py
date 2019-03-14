from agatereports.adapters import MysqlAdapter
from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def variables_system_sample():
    """
    Displaying variables such as row number and page number that are supported by the engine.

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.

    'PAGE_NUMBER': current page number in the report
    'REPORT_COUNT': current row number in the data source
    'PAGE_COUNT': current row number of the data source in a page
     """
    logger.info('running variables system sample')
    jrxml_filename = './jrxml/variables_system.jrxml'  # input jrxml filename
    output_filename = './output/variables_system.pdf'  # output pdf filename

    # MySQL datasource
    config = {'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source)
    pdf_page.generate_report()


if __name__ == '__main__':
    variables_system_sample()
