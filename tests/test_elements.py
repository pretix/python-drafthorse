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


def test_direct_datetime_roundtrip_keeps_time():
    el = DirectDateTimeElement(NS_RAM, "CreationDateTime")
    el._value = datetime(2024, 5, 3, 14, 30, 45)
    node = el.to_etree()
    assert node.text == "2024-05-03T14:30:45"

    parsed = DirectDateTimeElement(NS_RAM, "CreationDateTime").from_etree(node)
    assert parsed._value == datetime(2024, 5, 3, 14, 30, 45)


def test_direct_datetime_invalid_raises_in_strict_mode():
    node = ET.Element("{%s}CreationDateTime" % NS_RAM)
    node.text = "not-a-date"
    with pytest.raises(ValueError):
        DirectDateTimeElement(NS_RAM, "CreationDateTime").from_etree(node, strict=True)
