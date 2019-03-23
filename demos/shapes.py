from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def shapes_sample(jrxml_filename = './jrxml/shapes.jrxml', output_filename = './output/shapes.pdf'):
    """
    Shapes samples.
    """
    logger.info('running shapes sample')
    # jrxml_filename = './jrxml/shapes.jrxml'  # input jrxml filename
    # output_filename = './output/shapes.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    shapes_sample()
