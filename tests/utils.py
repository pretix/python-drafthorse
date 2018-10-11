import os

from lxml import etree

import drafthorse


def validate_xml(xmlout, schema):
    with open(os.path.join(os.path.dirname(drafthorse.__file__), 'schema', schema + '.xsd'), 'rb') as schema_file:
        schema_xml = schema_file.read()
    schema_root = etree.XML(schema_xml)
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema=schema)
    xml_root = etree.fromstring(xmlout, parser)
    return etree.tostring(xml_root, pretty_print=True)
