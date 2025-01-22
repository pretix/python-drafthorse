from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .accounting import (
    ApplicableTradeTax,
    BillingSpecifiedPeriod,
    ReceivableAccountingAccount,
    TradeAllowanceCharge,
)
from .container import Container
from .delivery import SupplyChainEvent
from .elements import Element
from .fields import (
    DecimalField,
    Field,
    MultiField,
    QuantityField,
    StringField,
)
from .note import IncludedNote
from .party import ShipToTradeParty, UltimateShipToTradeParty
from .product import TradeProduct
from .references import (
    InvoiceReferencedDocument,
    LineAdditionalReferencedDocument,
    LineBuyerOrderReferencedDocument,
    LineContractReferencedDocument,
    LineDeliveryNoteReferencedDocument,
    LineDespatchAdviceReferencedDocument,
    LineReceivingAdviceReferencedDocument,
    LineUltimateCustomerOrderReferencedDocument,
)


class AllowanceCharge(TradeAllowanceCharge):
    class Meta:
        namespace = NS_RAM
        tag = "AppliedTradeAllowanceCharge"


class GrossPrice(Element):
    amount = DecimalField(
        NS_RAM, "ChargeAmount", required=True, profile=COMFORT, _d="Bruttopreis"
    )
    basis_quantity = QuantityField(
        NS_RAM, "BasisQuantity", required=False, profile=COMFORT, _d="Preisbasismenge"
    )
    charge: Container = MultiField(AllowanceCharge, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "GrossPriceProductTradePrice"


class NetPrice(Element):
    amount = DecimalField(NS_RAM, "ChargeAmount", required=True, profile=COMFORT)
    basis_quantity = QuantityField(
        NS_RAM, "BasisQuantity", required=False, profile=COMFORT, _d="Preisbasismenge"
    )
    # TODO: IncludedTradeTax missing

    class Meta:
        namespace = NS_RAM
        tag = "NetPriceProductTradePrice"


class LineDocument(Element):
    line_id = StringField(NS_RAM, "LineID")
    line_status_code = StringField(NS_RAM, "LineStatusCode")
    line_status_reason_code = StringField(NS_RAM, "LineStatusReasonCode")
    notes: Container = MultiField(IncludedNote)

    class Meta:
        namespace = NS_RAM
        tag = "AssociatedDocumentLineDocument"


class LineAgreement(Element):
    buyer_order: LineBuyerOrderReferencedDocument = Field(
        LineBuyerOrderReferencedDocument, required=False, profile=EXTENDED
    )
    contract: LineContractReferencedDocument = Field(
        LineContractReferencedDocument, required=False, profile=EXTENDED
    )
    customer_order: LineUltimateCustomerOrderReferencedDocument = Field(
        LineUltimateCustomerOrderReferencedDocument, required=False, profile=EXTENDED
    )
    additional_references: Container = MultiField(
        LineAdditionalReferencedDocument, required=False, profile=COMFORT
    )
    gross: GrossPrice = Field(GrossPrice, required=False, profile=COMFORT)
    net: NetPrice = Field(NetPrice)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLineTradeAgreement"


class LineDelivery(Element):
    billed_quantity = QuantityField(
        NS_RAM, "BilledQuantity", required=True, profile=BASIC, _d="Menge, berechnet"
    )
    charge_free_quantity = QuantityField(
        NS_RAM,
        "ChargeFreeQuantity",
        required=False,
        profile=EXTENDED,
        _d="Menge, ohne Berechnung",
    )
    package_quantity = QuantityField(
        NS_RAM,
        "PackageQuantity",
        required=False,
        profile=EXTENDED,
        _d="Anzahl Packstücke",
    )
    ship_to: ShipToTradeParty = Field(
        ShipToTradeParty, required=False, profile=EXTENDED
    )
    ultimate_ship_to: UltimateShipToTradeParty = Field(
        UltimateShipToTradeParty, required=False, profile=EXTENDED
    )
    event: SupplyChainEvent = Field(
        SupplyChainEvent,
        required=False,
        profile=EXTENDED,
        _d="Detailinformationen zur tatsächlichen Lieferung",
    )
    despatch_advice: LineDespatchAdviceReferencedDocument = Field(
        LineDespatchAdviceReferencedDocument, required=False, profile=EXTENDED
    )
    receiving_advice: LineReceivingAdviceReferencedDocument = Field(
        LineReceivingAdviceReferencedDocument, required=False, profile=EXTENDED
    )
    delivery_note: LineDeliveryNoteReferencedDocument = Field(
        LineDeliveryNoteReferencedDocument, required=False, profile=EXTENDED
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLineTradeDelivery"


class LineSummation(Element):
    total_amount = DecimalField(
        NS_RAM, "LineTotalAmount", required=True, profile=COMFORT
    )
    total_allowance_charge = DecimalField(
        NS_RAM,
        "TotalAllowanceChargeAmount",
        required=False,
        profile=EXTENDED,
        _d="Gesamtbetrag der Zu- und Abschläge",
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeSettlementLineMonetarySummation"


class LineSettlement(Element):
    trade_tax: ApplicableTradeTax = Field(ApplicableTradeTax, required=False)
    period: BillingSpecifiedPeriod = Field(BillingSpecifiedPeriod, required=False)
    allowance_charge: Container = MultiField(
        TradeAllowanceCharge,
        required=False,
        _d="Schalter für Zu-/Abschlag",
    )
    monetary_summation: LineSummation = Field(
        LineSummation, required=False, profile=BASIC
    )
    invoice_referenced_document: Container = MultiField(
        InvoiceReferencedDocument,
        required=False,
        profile=EXTENDED,
        _d="Referenz auf die vorausgegangene Rechnung",
    )
    additional_referenced_document: LineAdditionalReferencedDocument = Field(
        LineAdditionalReferencedDocument, required=False, profile=COMFORT
    )
    accounting_account: ReceivableAccountingAccount = Field(
        ReceivableAccountingAccount,
        required=False,
        profile=COMFORT,
        _d="Detailinformationen zur Buchungsreferenz",
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLineTradeSettlement"


class LineItem(Element):
    document: LineDocument = Field(LineDocument, required=True)
    product: TradeProduct = Field(TradeProduct)
    agreement: LineAgreement = Field(LineAgreement)
    delivery: LineDelivery = Field(LineDelivery)
    settlement: LineSettlement = Field(LineSettlement, required=True)

    class Meta:
        namespace = NS_RAM
        tag = "IncludedSupplyChainTradeLineItem"
