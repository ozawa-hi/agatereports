import datetime
import re


def add_attr2attributes(element, attributes, prefix=None):
    """
    Add attributes of elements to 'attributes' dictionary.
    :param element:
    :param attributes:
    :param prefix:
    :return:
    """
    attr = element.get('attr')
    if attr is not None:
        for key, value in attr.items():
            if prefix is None:
                dict_key = key
            else:
                dict_key = prefix + key[0].upper() + key[1:]
            if value.isdigit():
                attributes[dict_key] = int(value)
            else:
                attributes[dict_key] = value
    # return attributes


def replace_fields(field_dict, expression, row_data, attributes):
    """
    Replace fields with value from data source.
    If the field is not in the database, do not replace.
    :param expression: text to be processed
    :param row_data: a row from data source
    :param attributes: attribute of the element being processed (i.e. 'isBlankWhenNull')
    :return: expression with $F{} replaced with values from data source when they exist
    """
    # global report_info

    if expression is None or row_data is None:
        return None
    else:
        # find all field keys in specified expression
        new_keys = [key[key.find("$F{") + 3:key.find("}")] for key in re.findall('\$F\{.*?\}', expression)]

        # if report_info.get('field_dict') is not None:
        if field_dict is not None:
            for key in new_keys:
                # data_type = report_info['field_dict'].get(key)
                data_type = field_dict.get(key)
                # TODO need to add more datatype
                if data_type == 'java.lang.Integer':
                    data_value = str(row_data.get(key, '$F{' + key + '}'))
                elif data_type == 'java.sql.Timestamp':
                    date_time = row_data.get(key, '$F{' + key + '}')
                    if type(date_time) is not datetime.datetime:
                        data_value = date_time
                    else:
                        data_value = 'datetime.datetime(' + str(date_time.year) + ',' + str(date_time.month) + ',' \
                                     + str(date_time.day) + ',' + str(date_time.hour) + ',' + str(date_time.minute)\
                                     + ',' + str(date_time.second) + ',' + str(date_time.microsecond) + ','\
                                     + str(date_time.tzinfo) + ')'
                else:
                    is_blank_when_null = attributes.get('isBlankWhenNull')
                    value = row_data.get(key, '$F{' + key + '}')
                    if is_blank_when_null and value is None:
                        # data_value = ''
                        return ''
                    else:
                        data_value = '"' + str(row_data.get(key, '$F{' + key + '}')) + '"'
                expression = expression.replace('$F{' + key + '}', data_value)
        return expression
        # try:
        #     return expression
        # except SyntaxError:
        #     return expression


def replace_variables(variables, expression, attributes):
    """
    Replace fields with value from data source.
    If the field is not in the database, do not replace.
    :param expression:
    :param row_data: a row from data source
    :param attributes:
    :return:
    """
    # global variables

    # str_expression = str(expression)
    # str_expression = expression
    # find all variable keys in specified expression
    new_keys = [key[key.find("$V{") + 3:key.find("}")] for key in re.findall('\$V\{.*?\}', expression)]

    for key in new_keys:
        var_info = variables.get(key)
        if var_info is None:
            data_value = '$V{' + key + '}'    # do not replace
        else:
            data_type = var_info.get('class')

            # TODO need to add more datatype
            if data_type == 'java.lang.Integer':
                data_value = str(var_info.get('value', '$V{' + key + '}'))
            elif data_type == 'java.sql.Timestamp':
                date_time = var_info.get('value', '$V{' + key + '}')
                if type(date_time) is not datetime.datetime:
                    data_value = date_time
                else:
                    data_value = 'datetime.datetime(' + str(date_time.year) + ',' + str(date_time.month) + ',' \
                                 + str(date_time.day) + ',' + str(date_time.hour) + ',' + str(date_time.minute) + ',' \
                                 + str(date_time.second) + ',' + str(date_time.microsecond) + ',' + str(
                        date_time.tzinfo) + ')'
            else:
                is_blank_when_null = attributes.get('isBlankWhenNull')
                value = var_info.get('value', '$V{' + key + '}')
                if is_blank_when_null and value is None:
                    # data_value = ''
                    return ''
                else:
                    data_value = '"' + str(var_info.get('value', '$V{' + key + '}')) + '"'
        expression = expression.replace('$V{' + key + '}', data_value)
    return expression


def replace_text(report, expression, row_data, attributes):
    """
    Replace Field and Variables with values ($F{} and $V{}) and evaluate expression.
    :param expression: text element to evaluate
    :param row_data: a row from data source
    :param attributes: attributes of text element to output
    :return: evaluated expression ready for output
    """
    expression = replace_fields(report.get('field_dict'), expression=expression, row_data=row_data, attributes=attributes)   # replace $F{} with values
    expression = replace_variables(report.get('variables'), expression, attributes)          # replace $V{} with values
    try:
        return eval(expression)
    except SyntaxError:
        return expression
    except NameError:
        return expression


def strip_fname(name):
    """
    strip wrapper (e.g. F${}, V${}, P${}) from name.
    :param element: name to string.
    :return: element name without wrapper.
    """
    return name[3:-1]


def convert2boolean(text):
    """
    Convert a string to a boolean type.
    :param text: text to convert to boolean
    :return: 'True' if text is 'true' (case ignored). 'False' otherwise.
    """
    return text is not None and text.lower() == 'true'
