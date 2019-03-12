from agatereports.sample.engine.basePage import BaseClass


def hello_world_sample():
    """
    Hello World sample.
    """
    print('running hello world sample')
    jrxml_filename = './jrxml/hello_world.jrxml'  # input jrxml filename
    output_filename = './output/hello_world.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    hello_world_sample()
