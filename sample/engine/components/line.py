from reportlab.lib import colors

from agatereports.sample.engine.bands.elements import process_reportElement, process_graphicElement
from agatereports.sample.engine.commonutilities import add_attr2attributes

"""
List of possible line styles.
"""
line_style_dict = {
    'Solid': (1),
    'Dashed': (6,3),
    'Dotted': (1,2),
    'Double': (1)
}


def set_pen_attr(element, attributes):
    """
    Set pen attributes.
    :param element:
    :param attributes:
    :return:
    """
    pen_attr = element.get('attr')
    if pen_attr is None:
        return {}
    else:
        return {
            'lineStyle': pen_attr.get('lineStyle'),
            'lineWidth': float(pen_attr.get('lineWidth', '0')),
            'lineColor': pen_attr.get('lineColor')
        }


def draw_line(report_info, x1, y1, x2, y2, line_style, line_width, line_color):
    """
    Draw a line on report_info.
    :param x1: start x coordinate
    :param y1: start y coordinate
    :param x2: end x coordinate
    :param y2: end y coordinate
    :param line_style: line style
    :param line_width: line width
    :param line_color: line color in #FFFFFF format
    """
    # global report

    report_info['canvas'].saveState()

    report_info['canvas'].setDash(line_style_dict.get(line_style, (1)))
    report_info['canvas'].setLineWidth(line_width)
    if line_color is not None:
        report_info['canvas'].setStrokeColor(colors.HexColor(line_color))
    report_info['canvas'].line(x1, y1, x2, y2)
    if line_style == 'Double':  # double line consists of wide solid line with thin white line in between
        report_info['canvas'].setLineWidth(line_width*0.5)
        report_info['canvas'].setStrokeColor(colors.HexColor('#FFFFFF'))
        report_info['canvas'].line(x1, y1, x2, y2)

    report_info['canvas'].restoreState()


def draw_diagonal_line(report, attributes, line_style, line_width, line_color):
    """
    Process to jrxml diagonal line.
    :param attributes: line attributes. Attributes from "reportElement" element.
    :param line_style: line style
    :param line_width: line width
    :param line_color: line color
    """
    if attributes.get('direction') is None:  # top down
        draw_line(report,
                  attributes['x'],
                  report['cur_y'] - attributes['y'],
                  attributes['x'] + attributes['width'],
                  report['cur_y'] - attributes['y'] - attributes['height'],
                  line_style, line_width, line_color)
    else:  # bottom up
        draw_line(report,
                  attributes['x'],
                  report['cur_y'] - attributes['y'] - attributes['height'],
                  attributes['x'] + attributes['width'],
                  report['cur_y'] - attributes['y'],
                  line_style, line_width, line_color)


def process_box_element(report, element, attributes):
    """
    Draw borders around a component.
    :param element: jrxml box element
    :param attributes:
    """
    # global report_info

    report['canvas'].saveState()

    borders = element.get('child')
    if borders is not None:
        cell_border = {}
        # find each border line attributes
        for pen_elements in borders:
            for pen_key, pen_value in pen_elements.items():
                if pen_key == 'pen':    # draw all borders
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:    # all borders
                        cell_border['top'] = pen
                        cell_border['left'] = pen
                        cell_border['bottom'] = pen
                        cell_border['right'] = pen
                elif pen_key == 'topPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['top'] = pen
                elif pen_key == 'leftPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['left'] = pen
                elif pen_key == 'bottomPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['bottom'] = pen
                elif pen_key == 'rightPen':
                    pen = set_pen_attr(pen_value, attributes)
                    if pen['lineWidth'] > 0:
                        cell_border['right'] = pen
        # draw each border lines
        # draw top
        if cell_border.get('top') is not None:
            draw_line(report,
                      attributes['x'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'],
                      cell_border['top']['lineStyle'], cell_border['top']['lineWidth'],
                      cell_border['top']['lineColor']
                      )
        # draw left
        if cell_border.get('left') is not None:
            draw_line(report,
                      attributes['x'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['left']['lineStyle'], cell_border['left']['lineWidth'],
                      cell_border['left']['lineColor']
                      )
        # draw bottom
        if cell_border.get('bottom') is not None:
            draw_line(report,
                      attributes['x'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['bottom']['lineStyle'], cell_border['bottom']['lineWidth'],
                      cell_border['bottom']['lineColor'])
        # draw right
        if cell_border.get('right') is not None:
            draw_line(report,
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'],
                      attributes['x'] + attributes['width'],
                      report['cur_y'] - attributes['y'] - attributes['height'],
                      cell_border['right']['lineStyle'], cell_border['right']['lineWidth'],
                      cell_border['right']['lineColor'])
    report['canvas'].restoreState()


def process_line(report, element, row_data):
    """
    Process jrxml line element.
    :param element: jrxml line element
    """
    line_element = element.get('child')
    if line_element is not None:
        reportElement = process_reportElement(report, line_element[0].get('reportElement'))  # get reportElement
        # get attributes on line element (e.g. "direction") to determine which direction to draw a line
        add_attr2attributes(element, reportElement)

        # set attributes from following graphicElement
        reportElement = process_graphicElement(report, line_element, reportElement)

        # set line attributes
        line_style = reportElement.get('lineStyle')
        line_width = float(reportElement.get('lineWidth', '1.0'))
        line_color = reportElement.get('lineColor')

        draw_diagonal_line(report, reportElement, line_style, line_width, line_color)
