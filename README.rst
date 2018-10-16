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
file, which can be done using the ``factur-x`` Python library. This library can be used to generate or parse the contents of this XML file.

By low-level, we mean that this library models the ZUGFeRD data model 1:1 without any further
abstractions or simplifications. You can set and parse all parameters defined in ZUGFeRD 1.0.

All output is validated against the official XSDs, but no validation of profile levels (basic, comfort, extended) is performed.

Usage
-----

Parsing::

    >>> from drafthorse.models.document import Document
    >>> samplexml = open("sample.xml", "rb").read()
    >>> doc = Document.parse(samplexml)
    >>> str(doc.trade.agreement.seller.name)
    'Lieferant GmbH'

Generating::

    >>> from datetime import date
    >>> from drafthorse.models.document import Document
    >>> from drafthorse.models.note import IncludedNote

    >>> doc = Document()
    >>> doc.context.guideline_parameter.id = "urn:ferd:CrossIndustryDocument:invoice:1p0:comfort"
    >>> doc.header.id = "RE1337"
    >>> doc.header.name = "RECHNUNG"
    >>> doc.header.type_code = "380"
    >>> doc.header.issue_date_time.value = date.today()
    >>> doc.header.languages.add("de")
    >>> note = IncludedNote()
    >>> note.content.add("Test Node 1")
    >>> doc.header.notes.add(n)
    >>> doc.trade.agreement.seller.name = "Lieferant GmbH"

    >>> doc.serialize()
    b'<?xml version="1.0" encoding="UTF-8"?><rsm:CrossIndustryDocument …'


Development
-----------

To run the included tests::

    pip install -r requirements_dev.txt
    py.test tests

To automatically sort your Imports as required by CI::

    pip install isort
    isort -rc .


Credits and License
-------------------

Maintainer: Raphael Michel <michel@rami.io>

License: Apache License 2.0
