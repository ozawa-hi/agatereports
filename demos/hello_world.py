from agatereports.sample.engine.basePage import BaseClass

"""
Hello World
"""

input_filename = '../demos/jrxml/hello_world.jrxml'  # input jrxml filename
output_filename = '../demos/output/hello_world.pdf'    # output pdf filename

pdf_page = BaseClass(jrxml_filename=input_filename, output_filename=output_filename)
pdf_page.generate_pdf()
