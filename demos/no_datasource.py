from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def no_datasource_sample(jrxml_filename = './jrxml/no_datasource.jrxml', output_filename = './output/no_datasource.pdf'):
    """
    No datasource sample.

    To display only static elements, data_source may be set to 'None' or omitted from BaseClass argument.
    """
    logger.info('running no datasource sample')
    # jrxml_filename = './jrxml/no_datasource.jrxml'  # input jrxml filename
    # output_filename = './output/no_datasource.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=None)
    # OR 'data_config' may be entirely omitted from the argument as in the statement below.
    # pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    no_datasource_sample()
