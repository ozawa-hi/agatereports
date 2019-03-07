# agatereports
Pure Python engine to generate reports from JasperReports jrxml file.
=======================================

Introduction
------------
AgateReports is a pure Python tool to generate reports without extensive coding.
Jaspersoft Studio can be used to graphically place location of elements in a report layout.
https://sourceforge.net/projects/jasperstudio/

This package aims to be a solution to following users:
- Python developers who want to create a report using GUI tool.
- Users who wants to create report layout visually with minimum programming and without using Java

Differences with JasperReports
------------------------------
- AgateReports use different components than JasperReports and there are minor differences. AgateReports components are based on modules such as ReportLab that are available in Python
- AgateReports ia able to use .ttc fonts

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
