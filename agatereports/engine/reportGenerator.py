from agatereports.adapters import CSVAdapter
from agatereports.adapters import MysqlAdapter
from agatereports.adapters import PostgresqlAdapter
from agatereports.engine.bands.bands import calc_column_footer_band_height, calc_page_footer_band_height,\
    process_bands
from agatereports.engine.bands.elements import process_jasperReport_element
from agatereports.engine.components.text import set_fonts
from agatereports.engine.jrxml2json import parse_jrxml
from agatereports.exports.pdf import create_canvas

try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

import os
import json
import logging
import logging.config

logger = logging.getLogger(__name__)

try:
    from agatereports.java import java_formatter
    java = True
except Exception:
    java = False

# TODO need to break this file into smaller files.
# TODO need performance improvement.


def setup_logging(
    default_path='./logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            log_config = json.load(f)
        logging.config.dictConfig(log_config)
    else:
        logging.basicConfig(level=default_level)


def generate_report(jrxml_filename, output_filename, data_config, fonts=None, report_type='pdf'):
    """
    Generate pdf file.
    :param jrxml_filename: name of jrxml file to use.
    :param output_filename: name of output pdf file.
    :param data_config: data source configutation dictionary
    :param fonts: font configuration list
    :param report_type: type of file to generate (currently, only 'pdf' is supported)
    """
    setup_logging()
    if input is None or jrxml_filename is None:
        logger.error('No report generated. Please specify jrxml filename and output filename to generate.')
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
        report_info['main_datasource'] = None
        if data_config is not None:
            data_adapter = data_config.pop('adapter')
            if data_adapter is None:
                logger.error("'adapter' should be specified in the data configuration:" + str(data_config))
            else:
                if data_adapter == 'mysql':
                    report_info['main_datasource'] = MysqlAdapter(**data_config)
                elif data_adapter == 'postgres':
                    report_info['main_datasource'] = PostgresqlAdapter(data_config.get('config'))
                elif data_adapter == 'csv':
                    report_info['main_datasource'] = CSVAdapter(data_config.get('filename'))
                else:
                    logger.error("'invalid data adapter:" + data_adapter
                                 + "'. Valid adapter are 'mysql', 'postgres', 'csv'.")
                    return

        jrxml_list = parse_jrxml(jrxml_filename)
        jasper_report_element = jrxml_list.get('jasperReport')
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
    filename = 'fonts'

    input_filename = '../../tests/jrxml/' + filename + '.jrxml'  # input jrxml filename
    report_filename = '../../tests/output/pdf_' + filename + '.pdf'

    # MySQL datasource configuration
    # config = {'adapter': 'mysql', 'host': 'localhost', 'user': 'python', 'password': 'python',
    #                'database': 'agatereports'}

    # Postgresql datasource configuration
    # config = {"adapter": "postgres",
    #                "config": "host='172.18.0.4' port='5432' dbname='agatereports' user='python' password='python'"}

    # CSV datasource configuration
    config = {'adapter': 'csv', 'filename': '../../tests/data/address.csv'}

    font_list = [
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

    generate_report(input_filename, report_filename, config, font_list)
