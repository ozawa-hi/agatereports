from agatereports.sample.engine.basePage import BaseClass

"""
Shapes samples.
WARNING: 'circle' element is not supported by JasperReports and jrxml file must manually be edited with a text editor.
It can be created by placing an 'ellipse' and then editing the jrxml file.
CAUTION: Editing jrxml manually would prevent Jaspersoft Studio to be unable to open the file again.
x,y = center of the circle, radius = radius of the circle
<circle>
	<reportElement x="50" y="340" radius="25" uuid="da72f307-18e0-42f3-a213-e2707f76da4c"/>
</circle>
"""

input_filename = '../demos/jrxml/shapes.jrxml'  # input jrxml filename
output_filename = '../demos/output/shapes.pdf'    # output pdf filename

pdf_page = BaseClass(jrxml_filename=input_filename, output_filename=output_filename)
pdf_page.generate_pdf()
