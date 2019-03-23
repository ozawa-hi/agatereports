from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def barcode_sample(jrxml_filename='./jrxml/barcode.jrxml', output_filename='./output/barcode.pdf'):
    """
    Barcode generation sample.
    """
    logger.info('running barcode sample')
    # jrxml_filename = './jrxml/barcode.jrxml'  # input jrxml filename
    # output_filename = './output/barcode.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    barcode_sample()
