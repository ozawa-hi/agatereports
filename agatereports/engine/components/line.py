from reportlab.lib import colors

from agatereports.engine.bands.elements import process_reportElement, process_graphicElement
from agatereports.engine.commonutilities import add_attr2attributes

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


def draw_line(report, x1, y1, x2, y2, line_style, line_width, line_color):
    """
    Draw a line on report_info.
    :param report: dictionary holding report information
    :param x1: start x coordinate
    :param y1: start y coordinate
    :param x2: end x coordinate
    :param y2: end y coordinate
    :param line_style: line style
    :param line_width: line width
    :param line_color: line color in #FFFFFF format
    """
    report['canvas'].saveState()

    report['canvas'].setDash(line_style_dict.get(line_style, (1)))
    if line_color is not None:
        report['canvas'].setStrokeColor(colors.HexColor(line_color))

    if line_style != 'Double':  # double line consists of wide solid line with thin white line in between
        report['canvas'].setLineWidth(line_width)
        report['canvas'].line(x1, y1, x2, y2)
    else:
        report['canvas'].setLineWidth(line_width*1.5)
        report['canvas'].line(x1, y1, x2, y2)
        report['canvas'].setLineWidth(line_width*0.7)
        report['canvas'].setStrokeColor(colors.HexColor('#FFFFFF'))
        report['canvas'].line(x1, y1, x2, y2)

    report['canvas'].restoreState()


def draw_diagonal_line(report, attributes, line_style, line_width, line_color):
    """
    Process to jrxml diagonal line.
    :param report: dictionary holding report information
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
    :param report: dictionary holding report information
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


def process_line(report, element):
    """
    Process jrxml line element.
    :param report: dictionary holding report information
    :param element: jrxml line element
    """
    line_element = element.get('child')
    if line_element is not None:
        report_element = process_reportElement(report, line_element[0].get('reportElement'))  # get reportElement
        # get attributes on line element (e.g. "direction") to determine which direction to draw a line
        add_attr2attributes(element, report_element)

        # set attributes from following graphicElement
        # reportElement = process_graphicElement(report, line_element, report_element)
        process_graphicElement(report, line_element, report_element)

        # set line attributes
        line_style = report_element.get('lineStyle')
        line_width = float(report_element.get('lineWidth', '1.0'))
        line_color = report_element.get('lineColor')

        draw_diagonal_line(report, report_element, line_style, line_width, line_color)
