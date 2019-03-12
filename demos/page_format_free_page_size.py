from agatereports.sample.engine.basePage import BaseClass


def page_format_free_page_size_sample():
    """
    Page format sample. Free page size.
    """
    print('running print format free page size sample')
    jrxml_filename = './jrxml/page_format_free_page_size.jrxml'  # input jrxml filename
    output_filename = './output/page_format_free_page_size.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    page_format_free_page_size_sample()
