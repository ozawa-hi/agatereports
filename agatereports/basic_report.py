from agatereports.engine import reportGenerator


class BasicReport:
    """"
    Base wrapper class to generate reports.
    """
    def __init__(self, jrxml_filename, output_filename, data_config=None, fonts=None, report_type='pdf'):
        self.jrxml_filename = jrxml_filename
        self.output_filename = output_filename
        self.data_config = data_config
        self.fonts = fonts
        self.report_type = report_type

    def generate_report(self):
        reportGenerator.generate_report(jrxml_filename=self.jrxml_filename, output_filename=self.output_filename,
                                        data_config=self.data_config, fonts=self.fonts, report_type=self.report_type)

    def set_report_type(self, report_type):
        self.report_type = report_type
