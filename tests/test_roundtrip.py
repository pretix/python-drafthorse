import lxml.etree
import os
import pytest
from difflib import unified_diff
from io import BytesIO
from pypdf import PdfReader
from xml.dom import minidom

from drafthorse.models.document import Document
from drafthorse.pdf import attach_xml
from drafthorse.utils import validate_xml

samples = [
    f
    for f in os.listdir(os.path.join(os.path.dirname(__file__), "samples"))
    if f.endswith(".xml")
]


def diff_xml(a, b):
    for line in unified_diff(a.splitlines(), b.splitlines()):
        print(line)


def prettify(xml, **kwargs):
    try:
        from lxml import etree
    except ImportError:
        reparsed = minidom.parseString(xml)
        return reparsed.toprettyxml(indent="\t")
    else:
        parser = etree.XMLParser(remove_blank_text=True, **kwargs)
        return etree.tostring(etree.fromstring(xml, parser), pretty_print=True)


@pytest.mark.parametrize("filename", samples)
def test_sample_roundtrip(filename):
    origxml = prettify(
        open(os.path.join(os.path.dirname(__file__), "samples", filename), "rb").read(),
        remove_comments=True,
    )
    if filename.split("_")[2] != "XRECHNUNG":
        schema = "FACTUR-X_" + filename.split("_")[2]
    else:
        schema = "FACTUR-X_EN16931"

    # Validate that the sample file is valid, otherwise the test is moot
    validate_xml(xmlout=origxml, schema=schema)

    # Attach the XML to an empty PDF doc
    with open(
        os.path.join(os.path.dirname(__file__), "samples", "Empty.pdf"), "rb"
    ) as f:
        original_pdf_bytes = f.read()

    created_pdf_bytes = attach_xml(original_pdf_bytes, origxml)

    # Read back the PDF. We don't support extensive parsing, but this way we can assert that metadata is at least present
    # and syntactically valid.
    pdf_reader = PdfReader(BytesIO(created_pdf_bytes))
    assert pdf_reader.xmp_metadata

    # Parse the sample file into our internal python structure
    doc = Document.parse(origxml)

    # Validate output XML and render a diff for debugging
    # skip first line (namespace order…)
    origxml = b"\n".join(origxml.split(b"\n")[1:]).decode().strip()
    try:
        generatedxml = prettify(doc.serialize(schema))
        generatedxml = b"\n".join(generatedxml.split(b"\n")[1:]).decode().strip()
        diff_xml(origxml, generatedxml)
    except lxml.etree.XMLSyntaxError:
        generatedxml = prettify(doc.serialize(None))
        generatedxml = b"\n".join(generatedxml.split(b"\n")[1:]).decode().strip()
        diff_xml(origxml, generatedxml)
        raise

    # Compare output XML
    assert origxml == generatedxml
