import logging
import os
from xml.dom import minidom

logger = logging.getLogger("drafthorse")


def prettify(xml):
    reparsed = minidom.parseString(xml)
    return reparsed.toprettyxml(indent="\t")


def validate_xml(xmlout, schema):
    try:
        from lxml import etree
    except ImportError:
        logger.warning("Could not validate output as LXML is not installed.")
        return xmlout
    schema = etree.XMLSchema(file=os.path.join(os.path.dirname(__file__), 'schema', schema + '.xsd'))
    parser = etree.XMLParser(schema=schema)
    xml_root = etree.fromstring(xmlout, parser)
    return etree.tostring(xml_root, pretty_print=True)
