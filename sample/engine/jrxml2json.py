"""
Jrxml2json.py converts jrxml to json format.
"""
try:
    import xml.etree.cElementTree as xml
except ImportError:
    import xml.etree.ElementTree as xml

import json

def strip_namespace(element):
    """
    strip namespace from the element name.
    :param element: etree element.
    :return: element name without a namespace.
    """
    return element.tag.split('}')[-1]


def get_child_dict(element):
    """
    recursively create a tuple of child, attribute, and value of the element.
    :param element: etree element
    :return: an list with tuple of child, attribute, and value of the element
    """
    child_list = list(append_child_elements(element))
    if len(child_list) > 0:
        yield ('child', child_list)
    if len(element.attrib) > 0:
        yield ('attr', element.attrib)
    if element.text is not None and len(element.text.strip()) > 0:
        yield ('value', element.text)


def append_child_elements(element):
    """
    recursively append dict of element and it's child, attribute, and value of the element.
    :param element: etree element
    :return: dictionary of element name and sttributes, child elements, and value
    """
    for child in element:
        yield dict([(strip_namespace(child), dict(get_child_dict(child)))])


def parse_jrxml(filename):
    """
    Parse input jrxml file and convert it to json format.
    :param filename: jrxml file to parse
    :return: content of jrxml file in json format
    """
    xml_doc = xml.parse(filename)
    root = xml_doc.getroot()

    band_dict = {}
    for band in root:
        band_name = strip_namespace(band)
        band_element = band_dict.get(band_name)
        if band_element is None:
            band_dict[band_name] = list([{band_name: dict(get_child_dict(band))}])
        else:
            band_element.extend(list([{band_name: dict(get_child_dict(band))}]))
        #     print(band_element)
            # band_dict.extend(list([{band_name: dict(get_child_dict(band))}]))

    return dict([(strip_namespace(root), {'attr': root.attrib, 'child': band_dict})])


def write2file(element, filename):
    """
    Write json to a file
    :param element: json element to write to a file
    :param filename: name of the output file
    :return: None
    """
    try:
        with open(filename,"w") as out_file:
            out_file.write(str(element))
    except IOError as err:
        print(err)


if __name__ == '__main__':
    filename = 'empty_report'
    input_filename = '../../test/jrxml/' + filename + '.jrxml'  # input jrxml filename
    output_filename = '../../test/output/' + filename + '.json'

    parsed_jrxml = parse_jrxml(input_filename)
    write2file(json.dumps(parsed_jrxml), output_filename)
    # print(json.dumps(parsed_jrxml, indent=2))



