import sys
from codecs import open
from os import path
from setuptools import find_packages, setup

from drafthorse import version

here = path.abspath(path.dirname(__file__))

try:
    # Get the long description from the relevant file
    with open(path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = f.read()
except:  # noqa
    long_description = ""

setup(
    name="drafthorse",
    version=version,
    description="Python ZUGFeRD XML implementation",
    long_description=long_description,
    url="https://github.com/pretix/python-drafthorse",
    author="Raphael Michel",
    author_email="michel@rami.io",
    license="Apache License",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="xml banking sepa",
    install_requires=["lxml", "PyPDF2"],
    packages=find_packages(include=["drafthorse", "drafthorse.*"]),
    include_package_data=True,
)
