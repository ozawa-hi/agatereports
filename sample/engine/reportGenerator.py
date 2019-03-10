try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

# import datetime
# import re

from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
#from reportlab.lib.pagesizes import landscape
# from reportlab.platypus import Paragraph, Table, TableStyle, KeepInFrame
# from reportlab.lib import colors

# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
# from PIL import Image

# from reportlab.graphics.barcode import code39, code128, code93
# from reportlab.graphics.barcode import eanbc, qr, usps, usps4s, common
# from reportlab.graphics.shapes import Drawing
# from reportlab.graphics import renderPDF

# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# from reportlab.lib.fonts import addMapping
# from reportlab import rl_config

from agatereports.sample.engine.jrxml2json import parse_jrxml
# from agatereports.jrxml.constants import constants
from agatereports.sample.adapters.MysqlAdapter import MysqlAdapter
from agatereports.sample.adapters.PostgresqlAdapter import PostgresqlAdapter
# import psycopg2
# from psycopg2.extras import DictCursor
from agatereports.sample.adapters.CSVAdapter import CSVAdapter
import collections

from agatereports.sample.engine.commonutilities import replace_text, add_attr2attributes

from agatereports.sample.exports.pdf import create_canvas, write_to_file
from agatereports.sample.engine.components.text import set_fonts
from agatereports.sample.engine.bands.bands import calc_column_footer_band_height, calc_page_footer_band_height
from agatereports.sample.engine.bands.elements import process_jasperReport_element

from agatereports.sample.engine.bands.bands import process_bands

try:
    from agatereports.java import java_formatter
    java = True
except:
    java = False

# TODO need to break this file into smaller files.
# TODO need performance improvement.


def generate_report(jrxml_filename, output_filename, data_source, fonts=None, report_type='pdf'):
    """
    Generate pdf file.
    :param jrxml_filename: name of jrxml file to use.
    :param output_filename: name of output pdf file.
    :param data_source:
    :parm fonts:
    """
    if input is None or jrxml_filename is None:
        print('please specify jrxml filename and output filename to generate.')
    else:
        report_info = dict(properties={},
                           variables={  # initial system variables
                               'PAGE_NUMBER': {'value': 1, 'class': 'java.lang.Integer'},
                               'MASTER_CURRENT_PAGE': {'value': None, 'class': 'java.lang.Integer'},
                               'MASTER_TOTAL_PAGES': {'value': None, 'class': 'java.lang.Integer'},
                               'COLUMN_NUMBER': {'value': 1, 'class': 'java.lang.Integer'},
                               'REPORT_COUNT': {'value': 0, 'class': 'java.lang.Integer'},
                               'PAGE_COUNT': {'value': 0, 'class': 'java.lang.Integer'},
                               'COLUMN_COUNT': {'value': 0, 'class': 'java.lang.Integer'}
                           },
                           pre_row_data={}, # previous row from datasource
                           row_data={}      # current row drom datasource
                           )

        report_info['main_datasource'] = data_source

        json = parse_jrxml(jrxml_filename)
        jasper_report_element = json.get('jasperReport')
        process_jasperReport_element(report_info, jasper_report_element)

        # create report_info
        report_info['output_filename'] = output_filename
        create_canvas(report_info)

        # set fonts if any
        report_info['available_fonts'] = set_fonts(fonts)

        # set band's element to global report_info[]
        bands = jasper_report_element.get('child')
        for key, value in bands.items():
            report_info[key] = value

        # set column footer and footer heights. This is used to calculate available height for details band.
        report_info['col_footer_height'] = calc_column_footer_band_height(report_info)
        report_info['page_footer_height'] = calc_page_footer_band_height(report_info)
        report_info['printingFooter'] = False    # flag to denote if printing out column and page footers

        process_bands(report_info, bands)


if __name__ == '__main__':
    filename = 'barcodes'

    input_filename = '../../tests/jrxml/' + filename + '.jrxml'  # input jrxml filename
    output_filename = '../../tests/output/pdf_' + filename + '.pdf'

    # MySQL datasource
    config = {'host': 'localhost', 'user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(**config)

    # Postgresql datasource
    # config = "host='172.17.0.2' port='5432' dbname='agatereports' user='python' password='python'"
    # data_source = PostgresqlAdapter(config)

    # CSV datasource
    # csv_filename = '../../tests/data/address.csv'
    # data_source = CSVAdapter(csv_filename)

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

    generate_report(input_filename, output_filename, data_source, fonts)
