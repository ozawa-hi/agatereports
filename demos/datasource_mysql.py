from agatereports.sample.adapters.MysqlAdapter import MysqlAdapter
from agatereports.sample.engine.basePage import BaseClass


def datasource_mysql_sample():
    """
    MySQL data source sample.

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    print('running datasource mysql sample')
    jrxml_filename = '../demos/jrxml/datasource_mysql.jrxml'  # input jrxml filename
    output_filename = '../demos/output/datasource_mysql.pdf'  # output pdf filename

    # MySQL datasource
    config = {'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_mysql_sample()