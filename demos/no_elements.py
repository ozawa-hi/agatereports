from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def no_elements_sample(jrxml_filename = './jrxml/no_elements.jrxml', output_filename = './output/no_elements.pdf'):
    """
    Hello World sample.
    """
    logger.info('running no elements sample')
    # jrxml_filename = './jrxml/no_elements.jrxml'  # input jrxml filename
    # output_filename = './output/no_elements.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    no_elements_sample()