from agatereports.sample.adapters.MysqlAdapter import MysqlAdapter
from agatereports.sample.adapters.PostgresqlAdapter import PostgresqlAdapter
from agatereports.sample.engine.basePage import BaseClass

"""
Test pdf generation.
"""
filenames = ['empty_report', 'no_data', 'text_fields', 'text_fields_lastPageFooter', 'shapes',
             'current_date', 'barcodes', 'pattern', 'when_no_data_All_sections_no_detail', 'when_no_data_Blank_page',
             'when_no_data_No_data_section', 'when_no_data_No_pages', 'when_no_data_Null', 'fonts', 'variables_system']

for filename in filenames:
    print('currently processing: ' + filename + '.jrxml')
    input_filename = '../tests/jrxml/' + filename + '.jrxml'  # input jrxml filename
    output_filename = '../tests/output/pdf_' + filename + '.pdf'    # output pdf filename
    fonts = [
        # list of additional directories to search for fonts
        {'font_path': ['../../tests/fonts/', '/usr/share/fonts/truetype/msttcorefonts/']},
        # Japanese font
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

    # MySQL datasource
    config = {'host': '172.18.0.2', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    # Postgresql datasource
    # config = "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"
    # data_source = PostgresqlAdapter(config)

    pdf_page = BaseClass(input_filename, output_filename, data_source, fonts)
    pdf_page.generate_report()
