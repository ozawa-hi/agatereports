from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def page_format_landscape_sample(jrxml_filename = './jrxml/page_format_landscape.jrxml', output_filename = './output/page_format_landscape.pdf'):
    """
    Page format sample. A4 landscape.
    """
    logger.info('running print format landscape sample')
    # jrxml_filename = './jrxml/page_format_landscape.jrxml'  # input jrxml filename
    # output_filename = './output/page_format_landscape.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_landscape_sample()
