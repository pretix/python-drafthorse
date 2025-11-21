import os
import pytest
import re
from pathlib import Path
from textwrap import dedent

README_PATH = Path(__file__).parent.parent / "README.rst"


@pytest.fixture
def invoice_document(request):
    readme = README_PATH.read_text(encoding="UTF-8")
    readme_example = re.search(
        "Generating::$" "(?P<example>.*)" "# Attach XML to an existing PDF.$",
        readme,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert readme_example
    local_ns = {}
    exec(dedent(readme_example["example"]), locals=local_ns)
    return local_ns['doc']


@pytest.fixture
def empty_pdf16_bytes():
    pdf_file = open(
        os.path.join(os.path.dirname(__file__), "samples", "empty_pdf16.pdf"), "rb"
    ).read()

    return pdf_file


@pytest.fixture
def invoice_pdf17_bytes():
    pdf_file = open(
        os.path.join(os.path.dirname(__file__), "samples", "invoice_pdf17.pdf"),
        "rb",
    ).read()

    return pdf_file
