from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def text_styles_sample(jrxml_filename = './jrxml/text_styles.jrxml', output_filename = './output/text_styles.pdf'):
    """
    Samples of different text styles.
    """
    logger.info('running text styles sample')
    # jrxml_filename = './jrxml/text_styles.jrxml'  # input jrxml filename
    # output_filename = './output/text_styles.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    text_styles_sample()
