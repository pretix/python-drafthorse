import os
import sys
from difflib import unified_diff

import pytest
import lxml.etree

from drafthorse.models.document import Invoice
from drafthorse.utils import prettify, validate_xml

samples = os.listdir(os.path.join(os.path.dirname(__file__), 'samples'))


def _diff_xml(a, b):
    for line in unified_diff(a.splitlines(), b.splitlines()):
        print(line)


@pytest.mark.parametrize("filename", samples)
def test_sample_roundtrip(filename):
    origxml = prettify(
        open(os.path.join(os.path.dirname(__file__), 'samples', filename), 'rb').read(),
        remove_comments=True
    )
    if filename.split('_')[2] != "XRECHNUNG":
        schema = 'FACTUR-X_' + filename.split('_')[2]
    else:
        schema = 'FACTUR-X_EN16931'

    # Validate that the sample file is valid, otherwise the test is moot
    validate_xml(xmlout=origxml, schema=schema)

    # Parse the sample file into our internal python structure
    doc = Invoice.parse(origxml)

    # Validate output XML and render a diff for debugging
    # skip first line (namespace order…)
    origxml = b"\n".join(origxml.split(b"\n")[1:]).decode().strip()
    try:
        generatedxml = prettify(doc.serialize(schema))
        generatedxml = b"\n".join(generatedxml.split(b"\n")[1:]).decode().strip()
        _diff_xml(origxml, generatedxml)
    except lxml.etree.XMLSyntaxError:
        generatedxml = prettify(doc.serialize(None))
        generatedxml = b"\n".join(generatedxml.split(b"\n")[1:]).decode().strip()
        _diff_xml(origxml, generatedxml)
        raise

    # Compare output XML
    assert origxml == generatedxml
