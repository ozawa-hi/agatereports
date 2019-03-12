from agatereports.sample.adapters.PostgresqlAdapter import PostgresqlAdapter
from agatereports.sample.engine.basePage import BaseClass


def datasource_postgresql_sample():
    """
    PostgreSQL data source sample.
    WARNING:Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/postgresql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    print('running datasource postgresql sample')
    jrxml_filename = '../demos/jrxml/datasource_postgresql.jrxml'  # input jrxml filename
    output_filename = '../demos/output/datasource_postgresql.pdf'  # output pdf filename

    # Postgresql datasource
    config = "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"
    data_source = PostgresqlAdapter(config)

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_postgresql_sample()
