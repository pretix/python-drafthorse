import xml.etree.ElementTree as ET

from drafthorse.models.product import ProductClassification

NS = "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"


def _parse(code, list_id, version):
    xml = (
        f'<ram:DesignatedProductClassification xmlns:ram="{NS}">'
        f'<ram:ClassCode listID="{list_id}" listVersionID="{version}">{code}</ram:ClassCode>'
        "</ram:DesignatedProductClassification>"
    )
    return ProductClassification().from_etree(ET.fromstring(xml))


def test_class_code_keeps_the_original_text():
    horses = _parse("010121", "HS", "2022")
    assert str(horses.class_code) == "010121 (HS 2022)"

    service = _parse("SRV", "ZZZ", "1")
    assert str(service.class_code) == "SRV (ZZZ 1)"
