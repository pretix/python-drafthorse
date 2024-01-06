import pytest

from drafthorse.pdf import attach_xml


@pytest.mark.parametrize("invoice_document", ["380"], indirect=True)
def test_readme_construction_example_pdf16(invoice_document, empty_pdf16_bytes):
    """
    Test using a PDF 1.6 version
    """
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")
    output_pdf = attach_xml(empty_pdf16_bytes, xml)

    assert output_pdf


@pytest.mark.parametrize("invoice_document", ["380"], indirect=True)
def test_readme_construction_example_pdf17(invoice_document, invoice_pdf17_bytes):
    """
    Test using a PDF 1.7 version in order to cover the output intents handling
    """
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")
    output_pdf = attach_xml(invoice_pdf17_bytes, xml)

    assert output_pdf


@pytest.mark.parametrize("invoice_document", ["220"], indirect=True)
def test_invalid_invoice_exceptions(invoice_document, invoice_pdf17_bytes):
    """
    Test invalid cases
    """
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")

    # invalid type code -> set order (220) instead of invoice (380)
    with pytest.raises(Exception) as exc_info:
        attach_xml(invoice_pdf17_bytes, xml)

    assert (
        str(exc_info.value)
        == "Invalid doc type! XML value for TypeCode shall be 380 for an invoice."
    )

    # invalid pdf type
    with pytest.raises(Exception) as exc_info:
        attach_xml("invalid_pdf_type", xml)

    assert str(exc_info.value) == "Please supply original PDF as bytes."

    # invalid xml type
    with pytest.raises(Exception) as exc_info:
        attach_xml(invoice_pdf17_bytes, "invalid_xml_type")

    assert str(exc_info.value) == "Please supply XML data as bytes."
