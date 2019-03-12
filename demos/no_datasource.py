from agatereports.sample.engine.basePage import BaseClass


def no_datasource_sample():
    """
    No datasource sample.

    To display only static elements, data_source may be set to 'None' or omitted from BaseClass argument.
    """
    print('running no datasource sample')
    jrxml_filename = './jrxml/no_datasource.jrxml'  # input jrxml filename
    output_filename = './output/no_datasource.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=None)
    # OR 'data_source' may be entirely omitted from the argument as in the statement below.
    # pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    no_datasource_sample()
