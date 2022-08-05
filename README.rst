drafthorse -- Basic ZUGFeRD implementation in Python
====================================================

.. image:: https://travis-ci.com/pretix/python-drafthorse.svg?branch=master
   :target: https://travis-ci.com/pretix/python-drafthorse

.. image:: https://codecov.io/gh/pretix/python-drafthorse/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pretix/drafthorse

.. image:: http://img.shields.io/pypi/v/drafthorse.svg
   :target: https://pypi.python.org/pypi/drafthorse

This is a low-level python implementation of the ZUGFeRD XML format. ZUGFeRD is a German
format for sending digital invoices. ZUGFeRD XML files are to be attached to a PDF
file. This library can be used to generate or parse the contents of this XML file as well as
attach it to a PDF. We do not support parsing PDF files (for now).

By low-level, we mean that this library tries to model the ZUGFeRD data model 1:1 without any
further abstractions or simplifications. You can set and parse all parameters defined in ZUGFeRD
2.2.

All output is validated against the official XSDs, but no validation of profile levels
(basic, comfort, extended) is performed.

Usage
-----

Parsing::

    from drafthorse.models.document import Document
    samplexml = open("sample.xml", "rb").read()
    doc = Document.parse(samplexml)
    print(doc.trade.agreement.seller.name)

Generating::

    import os
    from datetime import date
    from decimal import Decimal

    from drafthorse.models.accounting import ApplicableTradeTax
    from drafthorse.models.document import Document
    from drafthorse.models.note import IncludedNote
    from drafthorse.models.tradelines import LineItem
    from drafthorse.pdf import attach_xml

    # Build data structure
    doc = Document()
    doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended"
    doc.header.id = "RE1337"
    doc.header.type_code = "380"
    doc.header.name = "RECHNUNG"
    doc.header.issue_date_time = date.today()
    doc.header.languages.add("de")

    note = IncludedNote()
    note.content.add("Test Node 1")
    doc.header.notes.add(note)

    doc.trade.agreement.seller.name = "Lieferant GmbH"
    doc.trade.settlement.payee.name = "Kunde GmbH"

    doc.trade.agreement.buyer.name = "Kunde GmbH"
    doc.trade.settlement.invoicee.name = "Kunde GmbH"

    doc.trade.settlement.currency_code = "EUR"
    doc.trade.settlement.payment_means.type_code = "ZZZ"

    li = LineItem()
    li.document.line_id = "1"
    li.product.name = "Rainbow"
    li.agreement.gross.amount = Decimal("999.00")
    li.agreement.gross.basis_quantity = (Decimal("1.0000"), "C62")  # C62 == pieces
    li.agreement.net.amount = Decimal("999.00")
    li.agreement.net.basis_quantity = (Decimal("999.00"), "EUR")
    li.delivery.billed_quantity = (Decimal("1.0000"), "C62")  # C62 == pieces
    li.settlement.trade_tax.type_code = "VAT"
    li.settlement.trade_tax.category_code = "E"
    li.settlement.trade_tax.rate_applicable_percent = Decimal("0.00")
    li.settlement.monetary_summation.total_amount = Decimal("999.00")
    doc.trade.items.add(li)

    trade_tax = ApplicableTradeTax()
    trade_tax.calculated_amount = Decimal("0.00")
    trade_tax.basis_amount = Decimal("999.00")
    trade_tax.type_code = "VAT"
    trade_tax.category_code = "E"
    trade_tax.rate_applicable_percent = Decimal("0.00")
    doc.trade.settlement.trade_tax.add(trade_tax)

    doc.trade.settlement.monetary_summation.line_total = Decimal("999.00")
    doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
    doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
    doc.trade.settlement.monetary_summation.tax_basis_total = Decimal("999.00")
    doc.trade.settlement.monetary_summation.tax_total = Decimal("0.00")
    doc.trade.settlement.monetary_summation.grand_total = Decimal("999.00")
    doc.trade.settlement.monetary_summation.due_amount = Decimal("999.00")

    # Generate XML file
    xml = doc.serialize(schema="FACTUR-X_EXTENDED")

    # Attach XML to an existing PDF.
    # Note that the existing PDF should be compliant to PDF/A-3!
    # You can validate this here: https://www.pdf-online.com/osa/validate.aspx
    with open("input.pdf", "rb") as original_file:
        new_pdf_bytes = attach_xml(original_file.read(), xml, 'EXTENDED')

    with open("output.pdf", "wb") as f:
        f.write(new_pdf_bytes)


Development
-----------

To run the included tests::

    pip install -r requirements_dev.txt
    py.test tests

To automatically sort your Imports as required by CI::

    pip install isort
    isort -rc .

To validate files using mustang::

    git clone https://github.com/ZUGFeRD/mustangproject.git
    cd mustangproject
    git checkout core-2.5.1
    ./mvnw clean package
    java -jar Mustang-CLI/target/Mustang-CLI-2.5.1-SNAPSHOT.jar --action validate --source invoice.pdf


Credits and License
-------------------

Maintainer: Raphael Michel <michel@rami.io>

License of the Python code: Apache License 2.0

The PDF handling (drafthorse/pdf.py) is based on the code of factur-x, Copyright 2016-2018, Alexis de Lattre <alexis.delattre@akretion.com>,
released under a BSD license.

The packages includes schemas and samples of the ZUGFeRD specification (.xsd and .xml files) which are owned by the *Forum für elektronische Rechnungen bei der AWV e.V („FeRD“)* and are released under a proprietary license that allows bundling them together with other software for free.
