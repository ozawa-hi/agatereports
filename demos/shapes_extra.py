from agatereports.sample.engine.basePage import BaseClass


def shapes_extra_sample():
    """
    Shapes samples.
    WARNING: 'circle' element is not supported by JasperReports and jrxml file must manually be edited with a text editor.
    It can be created by placing an 'ellipse' and then editing the jrxml file.
    CAUTION: Editing jrxml manually would prevent Jaspersoft Studio to be unable to open the file again.
    """
    print('running shapes extra sample')
    jrxml_filename = './jrxml/shapes_extra.jrxml'  # input jrxml filename
    output_filename = './output/shapes_extra.pdf'    # output pdf filename

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename)
    pdf_page.generate_report()


if __name__ == '__main__':
    shapes_extra_sample()
