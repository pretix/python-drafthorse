import sys

from codecs import open
from os import path
from setuptools import find_packages, setup

from drafthorse import version

here = path.abspath(path.dirname(__file__))

try:
    # Get the long description from the relevant file
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:  # noqa
    long_description = ''

setup(
    name='drafthorse',
    version=version,
    description='Python ZUGFeRD XML implementation',
    long_description=long_description,
    url='https://github.com/pretix/pretix-drafthorse',
    author='Raphael Michel',
    author_email='michel@rami.io',
    license='Apache License',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='xml banking sepa',
    install_requires=[
                         'lxml'
                     ] + (['isoweek'] if sys.version_info < (3, 6) else []),

    packages=find_packages(include=['drafthorse', 'drafthorse.*']),
)
