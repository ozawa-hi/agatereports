from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def dates_sample(jrxml_filename = './jrxml/dates.jrxml', output_filename = './output/dates.pdf'):
    """
    Dates sample.
    WARNING: This sample uses MySQL database.
    Before running this sample, schema 'agatereports' must be create and populated.
    Run scripts in directory 'agatereports/tests/database/mysql' to create and populated database tables.

    Jaspersoft Studio is a Java application and uses Java classes and formats. It is necessary instead to use
    Python classes and formats in AgateReports.
    For example, today's date is retrieved using 'datetime.datetime.now()' instead of 'new java.util.Date()'
    Date/time format is specified using Python strftime formats. e.g. %Y-%m-%d
     """
    logger.info('running dates sample')
    # jrxml_filename = './jrxml/dates.jrxml'  # input jrxml filename
    # output_filename = './output/dates.pdf'  # output pdf filename

    # MySQL datasource
    config = {'adapter': 'mysql', 'host': 'localhost', 'user': 'python', 'password': 'python',
              'database': 'agatereports'}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=config)
    pdf_page.generate_report()


if __name__ == '__main__':
    dates_sample()
