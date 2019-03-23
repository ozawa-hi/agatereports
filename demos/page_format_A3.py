from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def page_format_A3_sample(jrxml_filename = './jrxml/page_format_A3.jrxml', output_filename = './output/page_format_A3.pdf'):
    """
    Page format sample. A3 sized page.
    """
    logger.info('running print format A3 sample')
    # jrxml_filename = './jrxml/page_format_A3.jrxml'  # input jrxml filename
    # output_filename = './output/page_format_A3.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_A3_sample()
