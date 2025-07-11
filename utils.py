from xml.etree import ElementTree as ET
import html


def xml_to_str(tree):
    ET.indent(tree, space='\t', level=0)
    tree = ET.tostring(tree, encoding='unicode', method='xml')
    return html.unescape(tree)


def bool2str(value: bool) -> str:
    if type(value) is bool:
        if value is True:
            return 'true'
        return 'false'
    else:
        raise ValueError('value must be True or False')