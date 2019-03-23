from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# TODO this should be made into a class with all write operations as a class method

def create_canvas(report):
    """
    Create a new reportLab canvas to generate pdf.
    :param report: dictionary holding report information

    """
    default_page_width, default_page_height = A4    # set default page siae to A4
    global page_width, page_height, cur_y

    page_width= report.get('pageWidth', default_page_width)
    page_height = report.get('pageHeight', default_page_height)
    cur_y = page_height

    report['canvas'] = canvas.Canvas(report['output_filename'], pagesize=(page_width, page_height))
    report['canvas'].setAuthor('AgateReports')
    report['canvas'].setTitle(report.get('name', 'sample report_info'))
    report['canvas'].setSubject(report.get('name', 'sample report_info'))


def write_to_file(report):
    """
    Start a new page and save current report_info to a file.
    :param report: dictionary holding report information
    """
    # save page to file
    if report.get('canvas') is not None:
        report['canvas'].showPage()  # start a new page
        report['canvas'].save()      # save to a file
