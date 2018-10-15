from drafthorse.models.delivery import SupplyChainEvent
from . import NS_FERD_1p0, BASIC, COMFORT, EXTENDED
from .accounting import TradeAllowanceCharge, BillingSpecifiedPeriod, AccountingAccount
from .elements import Element
from .fields import CurrencyField, QuantityField, Field, MultiField, StringField
from .note import IncludedNote
from .party import UltimateShipToTradeParty, ShipToTradeParty
from .product import TradeProduct
from .references import LineReceivingAdviceReferencedDocument, LineDespatchAdviceReferencedDocument, \
    LineDeliveryNoteReferencedDocument, LineCustomerOrderReferencedDocument, LineContractReferencedDocument, \
    LineBuyerOrderReferencedDocument, LineAdditionalReferencedDocument


class AllowanceCharge(TradeAllowanceCharge):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "AppliedTradeAllowanceCharge"


class GrossPrice(Element):
    amount = CurrencyField(NS_FERD_1p0, "ChargeAmount", required=True, profile=COMFORT,
                           _d="Bruttopreis")
    basis_quantity = QuantityField(NS_FERD_1p0, "BasisQuantity", required=False,
                                   profile=COMFORT, _d="Preisbasismenge")
    charge = Field(AllowanceCharge, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "GrossPriceProductTradePrice"


class NetPrice(Element):
    amount = CurrencyField(NS_FERD_1p0, "ChargeAmount", required=True, profile=COMFORT)
    basis_quantity = QuantityField(NS_FERD_1p0, "BasisQuantity", required=False,
                                   profile=COMFORT, _d="Preisbasismenge")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "NetPriceProductTradePrice"


class LineDocument(Element):
    line_id = StringField(NS_FERD_1p0, "LineID")
    notes = MultiField(IncludedNote)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AssociatedDocumentLineDocument"


class LineAgreement(Element):
    buyer_order = Field(LineBuyerOrderReferencedDocument, required=False, profile=EXTENDED)
    contract = Field(LineContractReferencedDocument, required=False, profile=EXTENDED)
    customer_order = Field(LineCustomerOrderReferencedDocument, required=False, profile=EXTENDED)
    additional_references = MultiField(LineAdditionalReferencedDocument, required=False,
                                       profile=COMFORT)
    gross = Field(GrossPrice, required=False, profile=COMFORT)
    net = Field(NetPrice)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeAgreement"


class LineDelivery(Element):
    billed_quantity = QuantityField(NS_FERD_1p0, "BilledQuantity", required=True,
                                    profile=BASIC, _d="Menge, berechnet")
    charge_free_quantity = QuantityField(NS_FERD_1p0, "ChargeFreeQuantity", required=False,
                                         profile=EXTENDED, _d="Menge, ohne Berechnung")
    package_quantity = QuantityField(NS_FERD_1p0, "ChargeFreeQuantity", required=False,
                                     profile=EXTENDED, _d="Anzahl Packstücke")
    ship_to = Field(ShipToTradeParty, required=False, profile=EXTENDED)
    ultimate_ship_to = Field(UltimateShipToTradeParty, required=False, profile=EXTENDED)
    event = Field(SupplyChainEvent, required=False, profile=EXTENDED,
                  _d="Detailinformationen zur tatsächlichen Lieferung")
    despatch_advice = Field(LineDespatchAdviceReferencedDocument, required=False,
                            profile=EXTENDED)
    receiving_advice = Field(LineReceivingAdviceReferencedDocument, required=False,
                             profile=EXTENDED)
    delivery_note = Field(LineDeliveryNoteReferencedDocument, required=False,
                          profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeDelivery"


class LineSummation(Element):
    total_amount = CurrencyField(NS_FERD_1p0, "LineTotalAmount", required=True,
                                 profile=COMFORT)
    total_allowance_charge = CurrencyField(NS_FERD_1p0, "TotalAllowanceChargeAmount",
                                           required=False, profile=EXTENDED, _d="Gesamtbetrag der Zu- und Abschläge")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementMonetarySummation"


class LineSettlement(Element):
    trade_tax = Field(LineAdditionalReferencedDocument, required=False, profile=COMFORT)
    period = Field(BillingSpecifiedPeriod, required=False, profile=EXTENDED)
    accounting_account = Field(AccountingAccount, required=False, profile=EXTENDED,
                               _d="Kostenstelle")
    monetary_summation = Field(LineSummation, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeSettlement"


class LineItem(Element):
    document = Field(LineDocument, required=True)
    agreement = Field(LineAgreement)
    delivery = Field(LineDelivery)
    settlement = Field(LineSettlement)
    product = Field(TradeProduct)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IncludedSupplyChainTradeLineItem"
