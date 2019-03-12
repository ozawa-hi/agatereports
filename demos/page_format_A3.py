from agatereports.sample.engine.basePage import BaseClass


def page_format_A3_sample():
    """
    Page format sample. A3 sized page.
    """
    print('running print format A3 sample')
    jrxml_filename = './jrxml/page_format_A3.jrxml'  # input jrxml filename
    output_filename = './output/page_format_A3.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_A3_sample()
