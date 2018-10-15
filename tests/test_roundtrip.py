import os

import pytest

from drafthorse.models.document import Document
from drafthorse.utils import prettify

samples = [
    'easybill_sample.xml',
    'ZUGFeRD_1p0_BASIC_Einfach.xml',
    'ZUGFeRD_1p0_BASIC_Rechnungskorrektur.xml',
    'ZUGFeRD_1p0_COMFORT_Einfach.xml',
    'ZUGFeRD_1p0_COMFORT_Haftpflichtversicherung_Versicherungssteuer.xml',
    'ZUGFeRD_1p0_COMFORT_Kraftfahrversicherung_Bruttopreise.xml',
    'ZUGFeRD_1p0_COMFORT_Rabatte.xml',
    'ZUGFeRD_1p0_COMFORT_Rechnungskorrektur.xml',
    'ZUGFeRD_1p0_COMFORT_Sachversicherung_berechneter_Steuersatz.xml',
    'ZUGFeRD_1p0_COMFORT_SEPA_Prenotification.xml',
    'ZUGFeRD_1p0_EXTENDED_Kostenrechnung.xml',
    'ZUGFeRD_1p0_EXTENDED_Rechnungskorrektur.xml',
    'ZUGFeRD_1p0_EXTENDED_Warenrechnung.xml',
]


@pytest.mark.parametrize("filename", samples)
def test_sample_roundtrip(filename):
    origxml = prettify(
        open(os.path.join(os.path.dirname(__file__), 'samples', filename), 'rb').read(),
        remove_comments=True
    )
    doc = Document.parse(origxml)
    generatedxml = prettify(doc.serialize())
    assert origxml.decode().strip() == generatedxml.decode().strip()
