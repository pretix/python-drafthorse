drafthorse -- Basic ZUGFeRD implementation in Python
====================================================

.. image:: https://travis-ci.org/pretix/drafthorse.svg?branch=master
   :target: https://travis-ci.org/pretix/drafthorse

.. image:: https://codecov.io/gh/pretix/drafthorse/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pretix/drafthorse

.. image:: http://img.shields.io/pypi/v/drafthorse.svg
   :target: https://pypi.python.org/pypi/drafthorse

This is a python implementation to generate the required XML for ZUGFeRD files

Limitations
-----------

Currently write-only.

Supported standards:

* ZUGFeRD 1.0

Supported profiles:

* Basic

Usage
-----

Example:

TBD


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
