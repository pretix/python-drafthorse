import logging
import os
from xml.dom import minidom

logger = logging.getLogger("drafthorse")


def minify(xml):
    try:
        from lxml import etree
        return b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + etree.tostring(etree.fromstring(xml))
    except ImportError:
        logger.warning("Could not minify output as LXML is not installed.")
        return xml


def prettify(xml, **kwargs):
    try:
        from lxml import etree
    except ImportError:
        reparsed = minidom.parseString(xml)
        return reparsed.toprettyxml(indent="\t")
    else:
        parser = etree.XMLParser(remove_blank_text=True, **kwargs)
        return b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + etree.tostring(
            etree.fromstring(xml, parser), pretty_print=True
        )


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
