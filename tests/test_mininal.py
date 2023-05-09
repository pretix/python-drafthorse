import pytest

from drafthorse.pdf import attach_xml


@pytest.mark.parametrize("invoice_document", ["380"], indirect=True)
def test_readme_construction_example(invoice_document, pdf_file_bytes):
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")
    output_pdf = attach_xml(pdf_file_bytes, xml)

    assert output_pdf


@pytest.mark.parametrize("invoice_document", ["220"], indirect=True)
def test_invalid_invoice_xml_order(invoice_document, pdf_file_bytes):
    # set order type code (220) instead of invoice (380)
    xml = invoice_document.serialize(schema="FACTUR-X_EXTENDED")
    with pytest.raises(Exception) as exc_info:
        attach_xml(pdf_file_bytes, xml)

    assert (
        str(exc_info.value)
        == "Invalid doc type! XML value for TypeCode shall be 380 for an invoice."
    )
