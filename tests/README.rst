tests directory contains files used to test AgateReports.
Tests are written using PyTest framework.

Contents of the directories are as follows:

==================================================      ==============================================================
File/Directory                                            Content
==================================================      ==============================================================
`test_agatereports.py <./test_agatereports.py>`_          pytest script to execute tests
`generate_test_pdf.py <./generate_test_pdf.py>`_          test execution scripts
`compare_results.py <./compare_results.py>`_              common test functions
`../data <../data>`_                                      data used in tests (e.g. csv datasource file)
`database <./database/README.rst>`_                       scripts to setup databases (e.g. MySQL, Postgres)
`fonts <./fonts>`_                                        font files used in test
`img <./img>`_                                            image file used in test
`output <./output>`_                                      generated reports
`output_demo <./output_demo>`_                            base demo reports to compare with for correctness
`output_original <./output_orignal>`_                     base reports to compare with for correctness
==================================================      ==============================================================

1. Executing Tests
Executing test_agatereports.py script will execute all the scripts in both tests directory and demos directory.

Tests directory currently contains tests with only jrxml files while demos directory contains py script for each jrxml
file. This planned to change so that demos directory contains only scripts and jrxml that'll show some unique feature
while tests directory may contain scripts and jrxml files that may test overlapping features.

Tests under tests directory may be selected by editing jrxml file names in list file names in generate_test_pdf function
in generate_test_pdf.py module.

A report may be generated from just one jrxml file by directly editing filename in
 agatereports.engine.reportGenerator.py

.. code-block:: python

    if __name__ == '__main__':
        filename = 'only_page_footer'

2. Maintaining Tests (to add more tests)
To add more tests, first decide to if tests should be in the demos directory or the tests directory. It there is a
script/jrxml with similar feature already in the demos directory, add the new test to the tests directory.

Place the jrxml file under the jrxml directory.
Generate and check the content of the report to make sure that it is correct. If it is correct, copy the pdf file to
output_original directory if the test is in the test directory or to the output_demo directory if the test is under
the demo directory. The pdf file will then be used to compare the result during further tests.

END

