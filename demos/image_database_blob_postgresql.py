from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_database_blob_postgresql_sample(jrxml_filename = './jrxml/image_database_blob.jrxml', output_filename = './output/image_database_blob_postgresql.pdf'):
    """
    Display an image saved as a blob in a postgresql database table column.

    WARNING: Before running this sample, database table 'pictures' must be create and populated.
    Run Python scripts in directory 'agatereports/tests/database/postgresql/create_pictures.py ' to create and
    populated database table.
    """
    logger.info('running image database blob sample')
    # jrxml_filename = './jrxml/image_database_blob.jrxml'  # input jrxml filename
    # output_filename = './output/image_database_blob_postgresql.pdf'    # output pdf filename

    # Postgresql datasource
    config = {"adapter": "postgres",
              "config": "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_database_blob_postgresql_sample()
