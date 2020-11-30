import os

import pytest

from drafthorse.models.document import Invoice
from drafthorse.utils import prettify

samples = os.listdir(os.path.join(os.path.dirname(__file__), 'samples'))


@pytest.mark.parametrize("filename", samples)
def test_sample_roundtrip(filename):
    origxml = prettify(
        open(os.path.join(os.path.dirname(__file__), 'samples', filename), 'rb').read(),
        remove_comments=True
    )
    doc = Invoice.parse(origxml)
    generatedxml = prettify(doc.serialize())
    assert origxml.decode().strip() == generatedxml.decode().strip()
