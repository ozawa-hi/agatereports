from agatereports.sample.engine.basePage import BaseClass


def text_styles_sample():
    """
    Samples of different text styles.
    """
    print('running text styles sample')
    jrxml_filename = './jrxml/text_styles.jrxml'  # input jrxml filename
    output_filename = './output/text_styles.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    text_styles_sample()
