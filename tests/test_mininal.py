import pytest

from drafthorse.pdf import attach_xml


@pytest.mark.parametrize("invoice_document", ["380"], indirect=True)
def test_readme_construction_example(invoice_document, pdf_file_bytes):
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")
    output_pdf = attach_xml(pdf_file_bytes, xml)

    assert output_pdf


@pytest.mark.parametrize("invoice_document", ["220"], indirect=True)
def test_invalid_invoice_xml(invoice_document, sample_invoice_pdf17):
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")

    # set order type code (220) instead of invoice (380)
    with pytest.raises(Exception) as exc_info:
        attach_xml(sample_invoice_pdf17, xml)

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
        attach_xml(sample_invoice_pdf17, "invalid_xml_type")

    assert str(exc_info.value) == "Please supply XML data as bytes."
