from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def image_workspace_sample(jrxml_filename = './jrxml/image_workspace.jrxml', output_filename = './output/image_workspace.pdf'):
    """
    Display an image in a workspace sample.
    """
    logger.info('running image workspace sample')
    # jrxml_filename = './jrxml/image_workspace.jrxml'  # input jrxml filename
    # output_filename = './output/image_workspace.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_workspace_sample()
