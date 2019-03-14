Demo Scripts
=======================================
This directory contains demos.

Content
------------
The demos are arranged in the following format:

=======================      ==============================================================
Directory                    Content
=======================      ==============================================================
.                            Python script to execute the demo
`./jrxml <./jrxml>`_         JasperReports jrxml files used in the demo
`./output <./output>`_       Executing the script will generate files in this directory
`./data <./data>`_           Sample data
=======================      ==============================================================

| jrxml files were created using Jaspersoft Studio.
| Community version can be obtained from Sourceforge. (Caution: 6.6.0 has some bugs and not recommended)
| https://sourceforge.net/projects/jasperstudio/files/JaspersoftStudio-6.5.1/

| Documentation on how to use Jaspersoft Studio is available in the following pages.
| https://community.jaspersoft.com/documentation/tibco-jaspersoft-studio-user-guide/v71/getting-started-jaspersoft-studio-0

| Demos: More detailed description of each demo is included in the .py file.
| All sample scripts can be executed by running `run_all_samples.py <`run_all_samples.py>`_ script.

1. Drawing basic report elements
    * `hello world.py <./hello_world.py>`_   - output a simple script to generate a report with text 'Hello World' |
    * `text_styles.py <./text_styles.py>`_  - text with various text properties (i.e. bold, italic, color, borders)

    * `fonts.py <./fonts.py>`_          - examples of specifying fonts
    * `shapes.py <./shapes.py>`_        - draw rectangles, ellipses, lines
    * `shapes_extra.py <./shapes_extra.py>`_  - draw circle (not supported by JasperReports)
    * `barcode.py <./barcode.py>`_       - display barcodes
    * `image.py <./image.py>`_         - display images

2. Outputting values retrieved from a datasource
    * `datasource_csv.py <./datasource_csv.py>`_        - display data read from a csv file
    * `datasource_mysql.py <./datasource_mysql.py>`_      - display data queried from MySQL database
    * `datasource_postgresql.py <./datasource_postgresql.py>`_  - display data queried from PostgreSQL database

3. Outputting variable values (e.g. row number, page number)
    * `variables_system.py <./variables_system.py>`_      - display system variable values

4. Formatting output
    * `dates_sample.py <./dates_sample.py>`_          - display date/time in different formats
    * `number_formatting.py <./number_formatting.py>`_     - formatting numbers, currency, percentage, scientific notation

5. Page size/orientation
    * `page_format_A3.py <./page_format_A3.py>`_            - generate report in size A3
    * `page_format_landscape.py <./page_format_landscape.py>`_     - generate report in landscape orientation
    * `page_format_free_page_size.py <./page_format_free_page_size.py>`_ - generate report in custom specified size
    * `page_format_margin.py <./page_format_margin.py>`_        - set margins on report

6. Text handling
    * `blank_when_null.py <./blank_when_null.py>`_           - display blank instead of 'None' in a field

7. Conditional data operations
    * `no_datasource.py <./no_datasource.py>`_             - when no datasource is specified (i.e. datasource is None)

8. following samples are when datasource is specified but there is no corresponding row
    * `when_no_data_null.py <./when_no_data_null.py>`_           - 'When No Data Type' is '<NULL>'
    * `when_no_data_no_pages.py <./when_no_data_no_pages.py>`_      - 'When No Data Type' is 'No Pages'
    * `when_no_data_blank_page.py <./when_no_data_blank_page.py>`_     - generate blank report
    * `when_no_data_all_sections_no_details.py <./when_no_data_all_sections_no_details.py>`_- 'When No Data Type' is 'All Sections No Details'
    * `when_no_data_no_data_section.py <./when_no_data_no_data_section.py>`_ - 'When No Data Type' is 'No Data Section'


Setup
----------------------
| Some of the demos use sample tables in MySQL and PostgreSQL databases.
| To run these demos, databases must be setup. Refer to `README.rst in the 'tests/database' directory <../tests/database/README.rst>`_ for further information.

Content of Each Script
----------------------
Demo py files mostly consists only of the following steps. These are the basic steps in AgateReports.
    1. specifying jrxml file (report layout file)
    2. name of output file name to generate
    3. defining fonts and datasource
    4. creating an instance of BaseClass class
    5. then calling 'generate_report'.


Example:

.. code-block:: python

    jrxml_filename = '../demos/jrxml/datasource_mysql.jrxml'  # 1. input jrxml filename
    output_filename = '../demos/output/datasource_mysql.pdf'  # 2. output pdf filename

    # 3. MySQL datasource
    config = {'host': 'localhost', 'port': '3306','user': 'python', 'password': 'python', 'database': 'agatereports'}
    data_source = MysqlAdapter(\**config)

    pdf_page = BaseClass(jrxml_filename=jrxml_filename, output_filename=output_filename, data_source=data_source) # 4. create BaseClass
    pdf_page.generate_report() # 5. generate report

END
