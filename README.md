# agatereports
Pure Python engine to generate reports from JasperReports jrxml file.
=======================================

Introduction
------------
AgateReports is a pure Python tool to generate reports from JasperReports jrxml file without needing to install Java.
This package aims to be a solution to following users:
- already have used JasperReports but now wants to migrate from Java to Python
- users who wants to create report layout visually with minimum programming and without using Java

Differences with JasperReports
------------------------------
- AgateReports use different components than JasperReports and there are minor differences. AgateReports uses components available in Python
- Java classes,pattern, and other Java syntax are not supported. For example, "Current Date" needs to be converted from "new java.util.Date()" to "datatime.datetime.now()"
- AgateReports is able to generate pdf file for each row in a datasource (this will minimize memory usage)
- AgateReports ia able to use .ttc fonts

Current Restrictions
--------------------
- AgateReports is still in initial development and does not provide all of JasperReports features.
  Only MySQL is supported as a datasource


Requirements
------------
Python3.6 or above
ReportLab
Pillow
MySQL Connector/Python
