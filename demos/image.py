from agatereports.sample.engine.basePage import BaseClass


def image_sample():
    """
    Image sample.
    """
    print('running image sample')
    jrxml_filename = './jrxml/image.jrxml'  # input jrxml filename
    output_filename = './output/image.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    image_sample()
