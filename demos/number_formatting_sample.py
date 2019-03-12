from agatereports.sample.adapters.MysqlAdapter import MysqlAdapter
from agatereports.sample.engine.basePage import BaseClass


def number_formatting_sample():
    """
    Jaspersoft Studio is a Java application that uses Java classes and format patterns. However, AgateReports is a
    Python application and uses Python classes and format patterns instead. That is, Python number formats such as
    '{:,}' and '{:.2f}' are used to format a number.
    Reference:
    https://docs.python.org/3.6/library/string.html

    WARNING: Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    CAUTION: Edit values of 'host' and 'port' to those in your environment.
     """
    print('running number formatting sample')
    jrxml_filename = '../demos/jrxml/number_formatting.jrxml'  # input jrxml filename
    output_filename = '../demos/output/number_formatting.pdf'  # output pdf filename

    # MySQL datasource
    config = {'host': 'localhost', 'port': '3306', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source)
    pdf_page.generate_report()


if __name__ == '__main__':
    number_formatting_sample()
