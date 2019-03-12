from agatereports.sample.adapters.CSVAdapter import CSVAdapter
from agatereports.sample.engine.basePage import BaseClass


def datasource_csv_sample():
    """
    CSV data source sample.
     """
    print('running datasource csv sample')
    jrxml_filename = '../demos/jrxml/datasource_csv.jrxml'  # input jrxml filename
    output_filename = '../demos/output/datasource_csv.pdf'    # output pdf filename

    # CSV datasource
    csv_filename = './data/product.csv'
    data_source = CSVAdapter(csv_filename)

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source)
    pdf_page.generate_report()


if __name__ == '__main__':
    datasource_csv_sample()
