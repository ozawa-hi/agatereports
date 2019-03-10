from agatereports.sample.engine.basePage import BaseClass

"""
Barcode generation sample.
"""

input_filename = '../demos/jrxml/barcodes.jrxml'  # input jrxml filename
output_filename = '../demos/output/barcodes.pdf'    # output pdf filename

pdf_page = BaseClass(jrxml_filename=input_filename, output_filename=output_filename)
pdf_page.generate_pdf()
