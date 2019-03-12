from agatereports.sample.engine.basePage import BaseClass


def barcode_sample():
    """
    Barcode generation sample.
    """
    print('running barcode sample')
    jrxml_filename = './jrxml/barcode.jrxml'  # input jrxml filename
    output_filename = './output/barcode.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    barcode_sample()
