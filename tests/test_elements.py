import xml.etree.cElementTree as ET
from datetime import datetime

import pytest

from drafthorse.models import NS_RAM
from drafthorse.models.container import IDContainer
from drafthorse.models.elements import ClassificationElement, DirectDateTimeElement


def test_classification_element_roundtrip_non_numeric_text():
    el = ClassificationElement(NS_RAM, "ClassCode")
    el._text = "ABC123"
    el._list_id = "TST"
    el._list_version_id = "1"
    node = el.to_etree()

    parsed = ClassificationElement(NS_RAM, "ClassCode").from_etree(node)
    assert parsed._text == "ABC123"
    assert parsed._list_id == "TST"
    assert parsed._list_version_id == "1"

