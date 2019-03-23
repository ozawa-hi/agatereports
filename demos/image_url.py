from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_url_sample(jrxml_filename = './jrxml/image_url.jrxml', output_filename = './output/image_url.pdf'):
    """
    Display an image from the Internet sample.
    """
    logger.info('running image url sample')
    # jrxml_filename = './jrxml/image_url.jrxml'  # input jrxml filename
    # output_filename = './output/image_url.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_url_sample()
