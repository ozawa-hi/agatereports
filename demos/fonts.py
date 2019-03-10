from agatereports.sample.engine.basePage import BaseClass

"""
Font samples.
"""

font_list = [
    # list of additional directories to search for fonts
    {'font_path': ['../tests/fonts/', '/usr/share/fonts/truetype/msttcorefonts/']},
    # Japanese font (ttc)
    {'font_filename': 'ipag.ttc',
     'fonts': [{'index': 0, 'name': 'IPAGothic'},
               {'index': 1, 'name': 'IPAPGothic'}
               ]},
    # tests/fonts
    {'font_filename': 'TIMES.TTF',
     'fonts': [{'index': 0, 'name': 'Times_New_Roman'}]},
    {'font_filename': 'TIMESBD.TTF',
     'fonts': [{'index': 1, 'name': 'Times_New_Roman-Bold'}]},
    {'font_filename': 'timesi.ttf',
     'fonts': [{'index': 2, 'name': 'Times_New_Roman-Italic'}]},
    {'font_filename': 'TIMESBI0.TTF',
     'fonts': [{'index': 3, 'name': 'Times_New_Roman-BoldItalic'}]},
    {'font-family':
         {'name': 'Times_New_Roman', 'normal': 'Times_New_Roman', 'bold': 'Times_New_Roman-Bold',
          'italic': 'Times_New_Roman-Italic', 'boldItalic': 'Times_New_Roman-BoldItalic'}
     },
    # tests/fonts. No index
    {'font_filename': 'Vera.ttf',
     'fonts': 'Vera'},
    {'font_filename': 'VeraBd.ttf',
     'fonts': 'Vera-Bold'},
    {'font_filename': 'VeraIt.ttf',
     'fonts': 'Vera-Italic'},
    {'font_filename': 'VeraBI.ttf',
     'fonts': 'Vera-BoldItalic'},
    {'font-family':
         {'name': 'Vera', 'normal': 'Vera', 'bold': 'Vera-Bold', 'italic': 'Vera-Italic',
          'boldItalic': 'Vera-BoldItalic'}
     },
    # ubuntu font
    {'font_filename': 'Verdana.ttf',
     'fonts': [{'index': 0, 'name': 'Verdana'}]},
    {'font_filename': 'Verdana_Bold.ttf',
     'fonts': [{'index': 1, 'name': 'Verdana-Bold'}]},
    {'font_filename': 'Verdana_Italic.ttf',
     'fonts': [{'index': 2, 'name': 'Verdana-Italic'}]},
    {'font_filename': 'Verdana_Bold_Italic.ttf',
     'fonts': [{'index': 3, 'name': 'Verdana-BoldItalic'}]},
    {'font-family':
         {'name': 'Verdana', 'normal': 'Verdana', 'bold': 'Verdana-Bold', 'italic': 'Verdana-Italic',
          'boldItalic': 'Verdana-BoldItalic'}
     }
]

input_filename = '../demos/jrxml/fonts.jrxml'  # input jrxml filename
output_filename = '../demos/output/fonts.pdf'    # output pdf filename

pdf_page = BaseClass(jrxml_filename=input_filename, output_filename=output_filename, fonts=font_list)
pdf_page.generate_pdf()