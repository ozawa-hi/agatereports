from agatereports.sample.engine.basePage import BaseClass

"""
Samples of different text styles.
"""

input_filename = '../demos/jrxml/text_styles.jrxml'  # input jrxml filename
output_filename = '../demos/output/text_styles.pdf'    # output pdf filename

pdf_page = BaseClass(jrxml_filename=input_filename, output_filename=output_filename)
pdf_page.generate_pdf()
