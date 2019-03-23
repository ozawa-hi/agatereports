from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_sample(jrxml_filename = './jrxml/image.jrxml', output_filename = './output/image.pdf'):
    """
    Image images in a local file system sample.
    """
    logger.info('running image sample')
    # jrxml_filename = './jrxml/image.jrxml'  # input jrxml filename
    # output_filename = './output/image.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_sample()
