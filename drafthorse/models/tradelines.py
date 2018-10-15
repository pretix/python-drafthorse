from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .accounting import (AccountingAccount, ApplicableTradeTax,
                         BillingSpecifiedPeriod, TradeAllowanceCharge)
from .delivery import SupplyChainEvent
from .elements import Element
from .fields import (CurrencyField, Field, MultiField, QuantityField,
                     StringField)
from .note import IncludedNote
from .party import ShipToTradeParty, UltimateShipToTradeParty
from .product import TradeProduct
from .references import (LineAdditionalReferencedDocument,
                         LineBuyerOrderReferencedDocument,
                         LineContractReferencedDocument,
                         LineCustomerOrderReferencedDocument,
                         LineDeliveryNoteReferencedDocument,
                         LineDespatchAdviceReferencedDocument,
                         LineReceivingAdviceReferencedDocument)


class AllowanceCharge(TradeAllowanceCharge):
    class Meta:
        namespace = NS_RAM
        tag = "AppliedTradeAllowanceCharge"


class GrossPrice(Element):
    amount = CurrencyField(NS_RAM, "ChargeAmount", required=True, profile=COMFORT,
                           _d="Bruttopreis")
    basis_quantity = QuantityField(NS_RAM, "BasisQuantity", required=False,
                                   profile=COMFORT, _d="Preisbasismenge")
    charge = MultiField(AllowanceCharge, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "GrossPriceProductTradePrice"


class NetPrice(Element):
    amount = CurrencyField(NS_RAM, "ChargeAmount", required=True, profile=COMFORT)
    basis_quantity = QuantityField(NS_RAM, "BasisQuantity", required=False,
                                   profile=COMFORT, _d="Preisbasismenge")

    class Meta:
        namespace = NS_RAM
        tag = "NetPriceProductTradePrice"


class LineDocument(Element):
    line_id = StringField(NS_RAM, "LineID")
    notes = MultiField(IncludedNote)

    class Meta:
        namespace = NS_RAM
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
        namespace = NS_RAM
        tag = "SpecifiedSupplyChainTradeAgreement"


class LineDelivery(Element):
    billed_quantity = QuantityField(NS_RAM, "BilledQuantity", required=True,
                                    profile=BASIC, _d="Menge, berechnet")
    charge_free_quantity = QuantityField(NS_RAM, "ChargeFreeQuantity", required=False,
                                         profile=EXTENDED, _d="Menge, ohne Berechnung")
    package_quantity = QuantityField(NS_RAM, "PackageQuantity", required=False,
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
        namespace = NS_RAM
        tag = "SpecifiedSupplyChainTradeDelivery"


class LineSummation(Element):
    total_amount = CurrencyField(NS_RAM, "LineTotalAmount", required=True,
                                 profile=COMFORT)
    total_allowance_charge = CurrencyField(NS_RAM, "TotalAllowanceChargeAmount",
                                           required=False, profile=EXTENDED, _d="Gesamtbetrag der Zu- und Abschläge")

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeSettlementMonetarySummation"


class LineSettlement(Element):
    trade_tax = Field(ApplicableTradeTax, required=False, profile=COMFORT)
    period = Field(BillingSpecifiedPeriod, required=False, profile=EXTENDED)
    accounting_account = Field(AccountingAccount, required=False, profile=EXTENDED,
                               _d="Kostenstelle")
    monetary_summation = Field(LineSummation, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedSupplyChainTradeSettlement"


class LineItem(Element):
    document = Field(LineDocument, required=True)
    agreement = Field(LineAgreement)
    delivery = Field(LineDelivery)
    settlement = Field(LineSettlement, required=True)
    product = Field(TradeProduct)

    class Meta:
        namespace = NS_RAM
        tag = "IncludedSupplyChainTradeLineItem"
