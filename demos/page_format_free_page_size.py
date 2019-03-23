from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def page_format_free_page_size_sample(jrxml_filename = './jrxml/page_format_free_page_size.jrxml', output_filename = './output/page_format_free_page_size.pdf'):
    """
    Page format sample. Free page size.
    """
    logger.info('running print format free page size sample')
    # jrxml_filename = './jrxml/page_format_free_page_size.jrxml'  # input jrxml filename
    # output_filename = './output/page_format_free_page_size.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_free_page_size_sample()
