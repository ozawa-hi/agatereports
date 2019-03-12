from agatereports.sample.engine.basePage import BaseClass


def page_format_landscape_sample():
    """
    Page format sample. A4 landscape.
    """
    print('running print format landscape sample')
    jrxml_filename = './jrxml/page_format_landscape.jrxml'  # input jrxml filename
    output_filename = './output/page_format_landscape.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_landscape_sample()
