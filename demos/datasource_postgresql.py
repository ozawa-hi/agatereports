from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def datasource_postgresql_sample(jrxml_filename = './jrxml/datasource_postgresql.jrxml', output_filename = './output/datasource_postgresql.pdf'):
    """
    PostgreSQL data source sample.
    WARNING:Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/postgresql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    logger.info('running datasource postgresql sample')
    # jrxml_filename = './jrxml/datasource_postgresql.jrxml'  # input jrxml filename
    # output_filename = './output/datasource_postgresql.pdf'  # output pdf filename

    # Postgresql datasource
    config = {"adapter": "postgres",
              "config": "host='172.18.0.4' port='5432'"
                        " dbname='agatereports' user='python' password='python'"}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_postgresql_sample()
