from . import BASIC, COMFORT, EXTENDED, NS_RAM, NS_FERD_1p0
from .accounting import (ApplicableTradeTax, AppliedTradeTax,
                         BillingSpecifiedPeriod, MonetarySummation,
                         ReceivableAccountingAccount, TradeAllowanceCharge)
from .delivery import TradeDelivery
from .elements import Element
from .fields import CurrencyField, Field, MultiField, StringField
from .party import (BuyerTradeParty, EndUserTradeParty, InvoiceeTradeParty,
                    PayeeTradeParty, SellerTradeParty)
from .payment import PaymentMeans, PaymentTerms
from .references import (AdditionalReferencedDocument,
                         BuyerOrderReferencedDocument,
                         ContractReferencedDocument,
                         CustomerOrderReferencedDocument)
from .tradelines import LineItem


class DeliveryTerms(Element):
    type_code = StringField(NS_RAM, "DeliveryTypeCode", required=False,
                            profile=EXTENDED, _d="Lieferbedingung (Code)")

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradeDeliveryTerms"


class TradeAgreement(Element):
    buyer_reference = StringField(NS_RAM, "BuyerReference", required=False,
                                  profile=COMFORT, _d="Referenz des Käufers")
    seller = Field(SellerTradeParty, required=True, _d="Detailinformationen zum Verkäufer")
    buyer = Field(BuyerTradeParty, required=True)
    end_user = Field(EndUserTradeParty, required=False, _d="Abweichender Endverbraucher")
    delivery_terms = Field(DeliveryTerms, required=False, profile=EXTENDED)
    buyer_order = Field(BuyerOrderReferencedDocument, required=False, profile=COMFORT)
    customer_order = Field(CustomerOrderReferencedDocument, required=False, profile=COMFORT)
    contract = Field(ContractReferencedDocument, required=False, profile=COMFORT)
    additional_references = MultiField(AdditionalReferencedDocument, required=False,
                                       profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableSupplyChainTradeAgreement"


class LogisticsServiceCharge(Element):
    description = StringField(NS_RAM, "Description", required=True, profile=COMFORT,
                              _d="Identifikation der Servicegebühr")
    applied_amount = CurrencyField(NS_RAM, "AppliedAmount", required=True,
                                   profile=COMFORT, _d="Betrag der Servicegebühr")
    trade_tax = MultiField(AppliedTradeTax, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLogisticsServiceCharge"


class TradeSettlement(Element):
    payment_reference = StringField(NS_RAM, "PaymentReference")
    currency_code = StringField(NS_RAM, "InvoiceCurrencyCode")
    invoicee = Field(InvoiceeTradeParty, required=False, profile=COMFORT,
                     _d="Rechnungsempfänger")
    payee = Field(PayeeTradeParty, required=False, profile=COMFORT,
                  _d="Zahlungsempfänger")
    payment_means = Field(PaymentMeans)
    trade_tax = MultiField(ApplicableTradeTax)
    period = Field(BillingSpecifiedPeriod, required=False, profile=COMFORT)
    allowance_charge = MultiField(TradeAllowanceCharge, required=False, profile=COMFORT,
                                  _d="Schalter für Zu-/Abschlag")
    service_charge = MultiField(LogisticsServiceCharge, required=False, profile=COMFORT)
    terms = MultiField(PaymentTerms, required=False, profile=COMFORT)
    money_summation = Field(MonetarySummation, required=True, profile=BASIC,
                            _d="Detailinformation zu Belegsummen")
    accounting_account = Field(ReceivableAccountingAccount, required=False, profile=EXTENDED,
                               _d="Detailinformationen zur Buchungsreferenz")

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableSupplyChainTradeSettlement"


class TradeTransaction(Element):
    agreement = Field(TradeAgreement, required=True)
    delivery = Field(TradeDelivery, required=True)
    settlement = Field(TradeSettlement, required=True)
    items = MultiField(LineItem, required=True)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeTransaction"
