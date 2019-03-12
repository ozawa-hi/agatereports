from agatereports.sample.engine.basePage import BaseClass


def shapes_sample():
    """
    Shapes samples.
    """
    print('running shapes sample')
    jrxml_filename = './jrxml/shapes.jrxml'  # input jrxml filename
    output_filename = './output/shapes.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    shapes_sample()
