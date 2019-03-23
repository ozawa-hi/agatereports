from agatereports.adapters import MysqlAdapter
from agatereports.adapters.PostgresqlAdapter import PostgresqlAdapter
from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_database_sample(jrxml_filename = './jrxml/image_database.jrxml', output_filename = './output/image_database.pdf'):
    """
    Display an image based on file path from a database table.
    """
    logger.info('running image database sample')
    # jrxml_filename = './jrxml/image_database.jrxml'  # input jrxml filename
    # output_filename = './output/image_database.pdf'    # output pdf filename

    # MySQL datasource configuration
    config = {'adapter': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python',
              'database': 'agatereports'}

    # # Postgresql datasource configuration
    # config = {"adapter": "postgres",
    #           "config": "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_database_sample()
