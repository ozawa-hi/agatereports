from agatereports.sample.engine import reportGenerator


class BaseClass:
    """"
    Base wrapper class to generate reports.
    """
    def __init__(self, jrxml_filename, output_filename, data_source=None, fonts=None, report_type='pdf'):
        self.jrxml_filename = jrxml_filename
        self.output_filename = output_filename
        self.data_source = data_source
        self.fonts = fonts
        self.report_type = report_type

    def generate_pdf(self):
        reportGenerator.generate_report(jrxml_filename=self.jrxml_filename, output_filename=self.output_filename,
                                        data_source=self.data_source, fonts=self.fonts, report_type=self.report_type)

    def set_report_type(self, report_type):
        self.report_type = report_type
