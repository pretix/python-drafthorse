import xml.etree.cElementTree as ET

from . import NS_RAM, NS_UDT, NS_FERD_1p0
from .elements import Element
from .fields import DateTimeField, Field, MultiField, StringField


class DocumentContextParameter(Element):
    id = StringField(NS_FERD_1p0, "ID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "GuidelineSpecifiedDocumentContextParameter"


class DocumentContext(Element):
    parameter = Field(DocumentContextParameter)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedExchangedDocumentContext"


class IncludedNote(Element):
    content = StringField(NS_FERD_1p0, "Content")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IncludedNote"


class IssueDateTime(Element):
    value = DateTimeField()

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IssueDateTime"


class Header(Element):
    id = StringField(NS_FERD_1p0, "ID")
    name = StringField(NS_FERD_1p0, "Name")
    type_code = StringField(NS_FERD_1p0, "TypeCode")
    issue_date_time = Field(IssueDateTime)
    notes = MultiField(IncludedNote)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "HeaderExchangedDocument"


class Document(Element):
    context = Field(DocumentContext)
    header = Field(Header)

    def __init__(self):
        super().__init__()
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace("rsm", NS_FERD_1p0)
        ET.register_namespace("ram", NS_RAM)
        ET.register_namespace("udt", NS_UDT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "CrossIndustryDocument"
