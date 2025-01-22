import xml.etree.cElementTree as ET

from .container import StringContainer, Container
from .note import IncludedNote

from . import BASIC, EXTENDED, NS_QDT, NS_RAM, NS_RSM, NS_UDT
from .elements import Element
from .fields import (
    DateTimeField,
    Field,
    IndicatorField,
    MultiField,
    MultiStringField,
    StringField,
)
from .trade import TradeTransaction


class GuidelineDocumentContextParameter(Element):
    id = StringField(NS_RAM, "ID")

    class Meta:
        namespace = NS_RAM
        tag = "GuidelineSpecifiedDocumentContextParameter"


class BusinessDocumentContextParameter(Element):
    id = StringField(NS_RAM, "ID")

    class Meta:
        namespace = NS_RAM
        tag = "BusinessProcessSpecifiedDocumentContextParameter"


class DocumentContext(Element):
    test_indicator = IndicatorField(
        NS_RAM, "TestIndicator", required=False, profile=EXTENDED, _d="Testkennzeichen"
    )
    business_parameter: BusinessDocumentContextParameter = Field(
        BusinessDocumentContextParameter,
        required=False,
        profile=EXTENDED,
        _d="Geschäftsprozess, Wert",
    )
    guideline_parameter: GuidelineDocumentContextParameter = Field(
        GuidelineDocumentContextParameter,
        required=True,
        profile=BASIC,
        _d="Anwendungsempfehlung",
    )

    class Meta:
        namespace = NS_RSM
        tag = "ExchangedDocumentContext"


class EffectivePeriod(Element):
    complete = DateTimeField(NS_RAM, "CompleteDateTime")

    class Meta:
        namespace = NS_RAM
        tag = "EffectiveSpecifiedPeriod"


class Header(Element):
    id = StringField(NS_RAM, "ID", required=True, profile=BASIC, _d="Rechnungsnummer")
    name = StringField(
        NS_RAM, "Name", required=True, profile=BASIC, _d="Dokumentenart (Freitext)"
    )
    type_code = StringField(
        NS_RAM, "TypeCode", required=True, profile=BASIC, _d="Dokumentenart (Code)"
    )
    issue_date_time = DateTimeField(
        NS_RAM, "IssueDateTime", required=True, profile=BASIC, _d="Rechnungsdatum"
    )
    copy_indicator = IndicatorField(
        NS_RAM,
        "CopyIndicator",
        required=False,
        profile=EXTENDED,
        _d="Indikator Original/Kopie",
    )
    languages: StringContainer = MultiStringField(
        NS_RAM, "LanguageID", required=False, profile=EXTENDED
    )
    notes: Container = MultiField(IncludedNote)
    effective_period = Field(
        EffectivePeriod,
        required=False,
        profile=EXTENDED,
        _d="Vertragliches Fälligkeitsdatum der Rechnung",
    )

    class Meta:
        namespace = NS_RSM
        tag = "ExchangedDocument"


class Document(Element):
    context: DocumentContext = Field(DocumentContext, required=True)
    header: Header = Field(Header, required=True)
    trade: TradeTransaction = Field(TradeTransaction, required=True)
    __namespaces = {
        "rsm": NS_RSM,
        "qdt": NS_QDT,
        "ram": NS_RAM,
        "xs": "http://www.w3.org/2001/XMLSchema",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "udt": NS_UDT,
    }

    def __init__(self):
        super().__init__()
        for ns, url in self.__namespaces.items():
            ET.register_namespace(ns, url)

    def serialize(self, schema="FACTUR-X_BASIC"):
        # First pass
        xml = super().serialize(schema)

        # Second pass to ensure all namespaces are defined even if they are unused
        root = ET.fromstring(xml)
        for ns, url in self.__namespaces.items():
            if ns.encode() not in xml:
                root.set(f"xmlns:{ns}", url)
        return ET.tostring(root, "utf-8")

    class Meta:
        namespace = NS_RSM
        tag = "CrossIndustryInvoice"
