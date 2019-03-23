# from agatereports.adapters.CSVAdapter import CSVAdapter
from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def datasource_csv_sample(jrxml_filename='./jrxml/datasource_csv.jrxml', output_filename='./output/datasource_csv.pdf'):
    """
    CSV data source sample.
     """
    logger.info('running datasource csv sample')
    # jrxml_filename = './jrxml/datasource_csv.jrxml'  # input jrxml filename
    # output_filename = './output/datasource_csv.pdf'    # output pdf filename

    # CSV datasource configuration
    data_config = {'adapter': 'csv', 'filename': '../data/product.csv'}

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, data_config=data_config)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_csv_sample()
