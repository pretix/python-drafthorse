import os

import pytest

from drafthorse.models.document import Document
from drafthorse.utils import prettify

samples = [
    'easybill_sample.xml',
]


@pytest.mark.parametrize("filename", samples)
def test_sample_roundtrip(filename):
    origxml = prettify(open(os.path.join(os.path.dirname(__file__), 'samples', filename), 'r').read())
    doc = Document.parse(origxml)
    generatedxml = prettify(doc.serialize())
    assert generatedxml.decode().strip() == origxml.decode().strip()