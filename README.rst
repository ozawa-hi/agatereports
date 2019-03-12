AgateReports

Pure Python engine to generate reports from JasperReports jrxml file.
==============================================================================

Introduction
------------
AgateReports is a pure Python tool to generate reports without extensive coding.
It currently relies on Jaspersoft Studio `<https://sourceforge.net/projects/jasperstudio/>`_ to graphically position reporting elements on a report layout.

This package aims to be a solution to following users:

- Python developers who want to create a report using GUI tool.
- Users who want to modify existing reports without programming.

Differences with JasperReports
------------------------------
- AgateReports use different components than JasperReports and there are minor differences. AgateReports components are based on modules such as ReportLab that are available in Python
- AgateReports ia able to use .ttc fonts
- Additional components available in Python are added. Currently, jrxml file must manually be edited to use these components. Furthermore, since JasperReports do not support these components, edited jrxml file can no longer be edited with Jaspersoft Studio. There is a plan to fork Jaspersoft Studio to support Python language syntax and these components.

Current Restrictions
--------------------
- AgateReports is still in initial development phase and does not provide all of JasperReports features.
- Patterns, format, and Java classes specified in jrxml file need to be changed to Python equivalent.
  For example, "Current Date" needs to be converted from "new java.util.Date()" to "datatime.datetime.now()"
- Currently, only MySQL, Postgresql, and csv file are supported as a datasource
- Performance is slow for large data source.


Requirements
------------
Python3.6 or above
ReportLab
Pillow
MySQL Connector/Python
psycopg2

Getting Started
----------------
- Installation - AgateReports is planned to be uploaded to PyPI. Steps will be added after successful upload.
- Usage - `demos directory <./demos/README.rst>`_ contains samples on how to use AgateReports.

END
