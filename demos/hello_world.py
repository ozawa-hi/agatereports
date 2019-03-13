from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def hello_world_sample():
    """
    Hello World sample.
    """
    logger.info('running hello world sample')
    jrxml_filename = './jrxml/hello_world.jrxml'  # input jrxml filename
    output_filename = './output/hello_world.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    hello_world_sample()
