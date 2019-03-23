from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_database_blob_mysql_sample(jrxml_filename = './jrxml/image_database_blob.jrxml', output_filename = './output/image_database_blob_mysql.pdf'):
    """
    Display an image saved as a blob in a mysql database table column.

    WARNING: Before running this sample, database table 'pictures' must be create and populated.
    Run Python scripts in directory 'agatereports/tests/database/mysql/create_pictures.py ' to create and
    populated database table.
    """
    logger.info('running image database blob sample')
    # jrxml_filename = './jrxml/image_database_blob.jrxml'  # input jrxml filename
    # output_filename = './output/image_database_blob_mysql.pdf'    # output pdf filename

    # MySQL datasource
    # WARNING: when handling blog columns, it is currently necessary to specify 'use_pure: True' attribute because
    #          of a bug in MySQL Connector bug.
    config = {'adapter': 'mysql', 'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python',
              'database': 'agatereports', 'use_pure': True}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_database_blob_mysql_sample()
