import xml.etree.cElementTree as ET

from drafthorse.models.note import IncludedNote

from . import BASIC, EXTENDED, NS_RAM, NS_UDT, NS_FERD_1p0
from .elements import Element
from .fields import (DateTimeField, Field, IndicatorField, MultiField,
                     MultiStringField, StringField)
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
    test_indicator = IndicatorField(NS_RAM, "TestIndicator", required=False,
                                    profile=BASIC, _d="Testkennzeichen")
    business_parameter = Field(BusinessDocumentContextParameter, required=False,
                               profile=EXTENDED, _d="Geschäftsprozess, Wert")
    guideline_parameter = Field(GuidelineDocumentContextParameter, required=True,
                                profile=BASIC, _d="Anwendungsempfehlung")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedExchangedDocumentContext"


class EffectivePeriod(Element):
    complete = DateTimeField(NS_RAM, "CompleteDateTime")

    class Meta:
        namespace = NS_RAM
        tag = "EffectiveSpecifiedPeriod"


class Header(Element):
    id = StringField(NS_RAM, "ID", required=True, profile=BASIC,
                     _d="Rechnungsnummer")
    name = StringField(NS_RAM, "Name", required=True, profile=BASIC,
                       _d="Dokumentenart (Freitext)")
    type_code = StringField(NS_RAM, "TypeCode", required=True, profile=BASIC,
                            _d="Dokumentenart (Code)")
    issue_date_time = DateTimeField(NS_RAM, "IssueDateTime", required=True,
                                    profile=BASIC, _d="Rechnungsdatum")
    copy_indicator = IndicatorField(NS_RAM, "CopyIndicator", required=False,
                                    profile=EXTENDED, _d="Indikator Original/Kopie")
    languages = MultiStringField(NS_RAM, "LanguageID", required=False, profile=EXTENDED)
    effective_period = Field(EffectivePeriod, required=False, profile=EXTENDED,
                             _d="Vertragliches Fälligkeitsdatum der Rechnung")
    notes = MultiField(IncludedNote)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "HeaderExchangedDocument"


class Document(Element):
    context = Field(DocumentContext, required=True)
    header = Field(Header, required=True)
    trade = Field(TradeTransaction, required=True)

    def __init__(self):
        super().__init__()
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace("rsm", NS_FERD_1p0)
        ET.register_namespace("ram", NS_RAM)
        ET.register_namespace("udt", NS_UDT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "CrossIndustryDocument"
