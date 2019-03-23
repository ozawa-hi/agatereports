from agatereports.basic_report import BasicReport

import logging
logger = logging.getLogger(__name__)


def fonts_sample(jrxml_filename = './jrxml/fonts.jrxml', output_filename = './output/fonts.pdf'):
    """
    Font samples.
    """
    logger.info('running fonts sample')
    font_list = [
        # list of additional directories to search for fonts
        {'font_path': ['../tests/fonts/', '/usr/share/fonts/truetype/msttcorefonts/']},
        # Japanese font (ttc).
        # 'font_filename' is the name of the ttc file
        # 'index' is the subfontIndex.
        # 'name' if the font name
        {'font_filename': 'ipag.ttc',
         'fonts': [{'index': 0, 'name': 'IPAGothic'},
                   {'index': 1, 'name': 'IPAPGothic'}
                   ]},
        # specifying normal, bold, italic, bold italic fonts as a single font family.
        # It is necessary to specify these 4 fonts in a font family.
        # When a font family name is specified in the report, selecting bold and italic attributes will cause to
        # automatically select the appropriate font in the family.
        # 'file_filename' is the name of the ttf file

        {'font_filename': 'TIMES.TTF',      # normal font
         'fonts': [{'index': 0, 'name': 'Times_New_Roman'}]},
        {'font_filename': 'TIMESBD.TTF',    # bold font
         'fonts': [{'index': 1, 'name': 'Times_New_Roman-Bold'}]},
        {'font_filename': 'timesi.ttf',     # italic font
         'fonts': [{'index': 2, 'name': 'Times_New_Roman-Italic'}]},
        {'font_filename': 'TIMESBI0.TTF',   # bold + italic font
         'fonts': [{'index': 3, 'name': 'Times_New_Roman-BoldItalic'}]},
        # 'name' is the font name to use in the report
        # 'normal', 'bold', 'italic', and 'boldItalic' are names of fonts specified above.
        {'font-family':
             {'name': 'Times_New_Roman', 'normal': 'Times_New_Roman', 'bold': 'Times_New_Roman-Bold',
              'italic': 'Times_New_Roman-Italic', 'boldItalic': 'Times_New_Roman-BoldItalic'}
         },
        # font family. 'index' may be omitted when using ttf fonts
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
        # ubuntu font - example of specifying fonts installed in Ubuntu directory
        # '/usr/share/fonts/truetype/msttcorefonts/'
        # It is still necessary to define font family to get bold, italic, bold italic attributes on fonts
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

    # jrxml_filename = './jrxml/fonts.jrxml'  # input jrxml filename
    # output_filename = './output/fonts.pdf'    # output pdf filename

    pdf_page = BasicReport(jrxml_filename=jrxml_filename, output_filename=output_filename, fonts=font_list)
    pdf_page.generate_report()


if __name__ == '__main__':
    fonts_sample()
