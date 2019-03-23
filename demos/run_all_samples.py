from demos.barcode import barcode_sample
from demos.blank_when_null import blank_when_null_sample
from demos.datasource_csv import datasource_csv_sample
from demos.datasource_mysql import datasource_mysql_sample
from demos.datasource_postgresql import datasource_postgresql_sample
from demos.dates import dates_sample
from demos.fonts import fonts_sample
from demos.hello_world import hello_world_sample
from demos.image import image_sample
from demos.image_url import image_url_sample
from demos.image_workspace import image_workspace_sample
from demos.image_database import image_database_sample
from demos.image_database_blob_mysql import image_database_blob_mysql_sample
from demos.image_database_blob_postgresql import image_database_blob_postgresql_sample
from demos.no_datasource import no_datasource_sample
from demos.no_elements import no_elements_sample
from demos.number_formatting import number_formatting_sample
from demos.page_format_A3 import page_format_A3_sample
from demos.page_format_landscape import page_format_landscape_sample
from demos.page_format_free_page_size import page_format_free_page_size_sample
from demos.page_format_margin import page_format_margin_sample
from demos.shapes import shapes_sample
from demos.shapes_extra import shapes_extra_sample
from demos.text_styles import text_styles_sample
from demos.variables_system import variables_system_sample
from demos.when_no_data_all_sections_no_details import when_no_data_all_sections_no_details_sample
from demos.when_no_data_blank_page import when_no_data_blank_page_sample
from demos.when_no_data_no_pages import when_no_data_no_pages_sample
from demos.when_no_data_null import when_no_data_null_sample
from demos.when_no_data_no_data_section import when_no_data_no_data_section_sample


def run_all_demos():
    """
    This script will run all the sample scripts.
    Some sample use MySQL and PostgreSQL databases. If the database is unavailable,
    those samples will error and corresponding reports will be generated.
    """
    hello_world_sample()    # display 'hello world'
    text_styles_sample()    # display different text styles (e.g. font size, borders, underlined, strike through)
    fonts_sample()          # load font files and display in those fonts

    shapes_sample()         # draw rectangles, ellipses, lines
    shapes_extra_sample()   # draw circle (not supported by JasperReports)
    barcode_sample()        # display barcodes

    image_sample()              # display images from local file system
    image_url_sample()          # display an image from Internet
    image_workspace_sample()    # display an image from workspace
    image_database_sample()                  # display images corresponding to filename saved in database table
    image_database_blob_mysql_sample()       # display images saved in mysql database table
    image_database_blob_postgresql_sample()  # display images saved in postgresql database table

    datasource_csv_sample()         # display data read from a csv file
    datasource_mysql_sample()       # display data queried from MySQL database
    datasource_postgresql_sample()  # display data queried from PostgreSQL database

    variables_system_sample()       # display system variable values

    dates_sample()                  # display date/time in different formats
    number_formatting_sample()      # formatting numbers, currency, percentage, scientific notation

    page_format_A3_sample()             # generate report in size A3
    page_format_landscape_sample()      # generate report in landscape orientation
    page_format_free_page_size_sample() # generate report in custom specified size
    page_format_margin_sample()         # set margins on report

    blank_when_null_sample()            # display blank instead of 'None' in a field

    no_datasource_sample()              # when no datasource is specified (i.e. datasource is None)
    no_elements_sample()                # when there is no elements in jrxml layout

    # following samples are when datasource is specified but there is no corresponding row
    when_no_data_null_sample()            # 'When No Data Type' is '<NULL>'
    when_no_data_no_pages_sample()        # 'When No Data Type' is 'No Pages'
    when_no_data_blank_page_sample()      # generate blank report
    when_no_data_all_sections_no_details_sample() # 'When No Data Type' is 'All Sections No Details'
    when_no_data_no_data_section_sample() # 'When No Data Type' is 'No Data Section'


if __name__ == '__main__':
    run_all_demos()

