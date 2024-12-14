import logging
import os

logger = logging.getLogger("drafthorse")


def validate_xml(xmlout, schema):
    try:
        from lxml import etree
    except ImportError:
        logger.warning("Could not validate output as LXML is not installed.")
        return xmlout
    if schema is not None:
        if schema.startswith("FACTUR-X_"):
            schema = schema.replace("FACTUR-X_", "Factur-X_1.0.07_")
            schema = schema.replace("BASIC-WL", "BASICWL")
        schema = etree.XMLSchema(
            file=os.path.join(os.path.dirname(__file__), "schema", schema + ".xsd")
        )
    parser = etree.XMLParser(schema=schema)
    xml_root = etree.fromstring(xmlout, parser)

    return etree.tostring(
        xml_root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
    )
