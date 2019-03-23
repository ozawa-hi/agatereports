from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def datasource_mysql_sample(jrxml_filename = './jrxml/datasource_mysql.jrxml', output_filename = './output/datasource_mysql.pdf'):
    """
    MySQL data source sample.

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    logger.info('running datasource mysql sample')
    # jrxml_filename = './jrxml/datasource_mysql.jrxml'  # input jrxml filename
    # output_filename = './output/datasource_mysql.pdf'  # output pdf filename

    # MySQL datasource
    config = {'adapter': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python',
              'database': 'agatereports'}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_mysql_sample()
