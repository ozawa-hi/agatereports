===========================
*report* Dictionary Keys
===========================

Data Source
---------------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
field_names                                             list of field names as declared in **field** band
main_datasource                                         datasource. None is no datasource. e.g. MysqlAdapter())
row_data												dict((field, value) for field, value in zip(report['field_names'], row))
==================================================      ==============================================================

Canvas
--------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
output_to_canvas                                        True if something was written to a canvas. Otherwise, False
canvas                                                  reportlab canvas to generate a page
cur_y													current y axis
available_fonts                                         fonts available to use
output_filename                                         name of file to generate
col_footer_height                                       height of column footer band
page_footer_height                                      height of page footer band
printingFooter                                          True is printing footer bands. Otherwise, False
==================================================      ==============================================================

group
-------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
group_names                                             dictionary of group names and values in jrxml.
                                                        e.g. {'name', '$F{city}'}
group_cur                                               list (stack) of group names.


jrxml Bands (key will only exist if corresponding element is included in jrxml
------------------------------------------------------------------------------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
background
columnFooter
columnHeader
detail
field
filterExpression
group
import
lastPageFooter
noData
pageFooter
pageHeader
parameter
property
queryString
reportFont
sortField
style
subDataset
summary
template
title
variable
==================================================      ==============================================================


jrxml Elements
-------------------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
pre_row_data											{}
properties												{}
row_data												{}
variables
	- PAGE_NUMBER                                       {'value': 1, 'class': 'java.lang.Integer'}
	- MASTER_CURRENT_PAGE								{'value': None, 'class': 'java.lang.Integer'}
	- MASTER_TOTAL_PAGES								{'value': None, 'class': 'java.lang.Integer'}
	- COLUMN_NUMBER										{'value': 1, 'class': 'java.lang.Integer'}
	- REPORT_COUNT										{'value': 0, 'class': 'java.lang.Integer'}
	- PAGE_COUNT										{'value': 0, 'class': 'java.lang.Integer'},
	- COLUMN_COUNT										{'value': 0, 'class': 'java.lang.Integer'}
==================================================      ==============================================================


Page Attributes
----------------
==================================================      ==============================================================
Element name                                             Content
==================================================      ==============================================================
bottomMargin											(default: '30')
columnCount												(default: '1')
columnSpacing											(default: '0')
columnWidth												(default: '555')
formatFactoryClass										(default: '')
isFloatColumnFooter										(default: 'false')
isIgnorePagination										(default: 'false')
isSummaryNewPage										(default: 'false')
isTitleNewPage											(default: 'false')
language script language								(e.g. python)
leftMargin												(default: '20')
name													(default: '')
orientation 											(default: 'Portrait')
pageWidth   											(default: A4 width=595)
pageHeight												(default: A4 height=842)
printOrder  											(default: 'Vertical')
resourceBundle 											(default:'')
rightMargin 											(default: '20')
scriptletClass 											(default: '')
topMargin 												(default: '30')
whenNoDataType 											(default: 'Null')
whenResourceMissingType 								(default: 'Null')
==================================================      ==============================================================

