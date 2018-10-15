from . import NS_FERD_1p0, COMFORT, EXTENDED, BASIC
from .accounting import ApplicableTradeTax, BillingSpecifiedPeriod, MonetarySummation, \
    AccountingAccount
from .accounting import TradeAllowanceCharge
from .delivery import TradeDelivery
from .elements import Element
from .fields import Field, MultiField, StringField, CurrencyField
from .party import PayeeTradeParty, SellerTradeParty, BuyerTradeParty, \
    EndUserTradeParty, InvoiceeTradeParty
from .payment import PaymentMeans, PaymentTerms
from .references import CustomerOrderReferencedDocument, ContractReferencedDocument, BuyerOrderReferencedDocument, \
    AdditionalReferencedDocument
from .tradelines import LineItem


class TradeAgreement(Element):
    buyer_reference = StringField(NS_FERD_1p0, "BuyerReference", required=False,
                                  profile=COMFORT, _d="Referenz des Käufers")
    seller = Field(SellerTradeParty, required=True, _d="Detailinformationen zum Verkäufer")
    buyer = Field(BuyerTradeParty, required=True)
    end_user = Field(EndUserTradeParty, required=False, _d="Abweichender Endverbraucher")
    delivery_type_code = StringField(NS_FERD_1p0, "DeliveryTypeCode", required=False,
                                     profile=EXTENDED, _d="Lieferbedingung (Code)")
    buyer_order = BuyerOrderReferencedDocument(required=False, profile=COMFORT)
    customer_order = CustomerOrderReferencedDocument(required=False, profile=COMFORT)
    contract = ContractReferencedDocument(required=False, profile=COMFORT)
    additional_references = MultiField(AdditionalReferencedDocument, required=False,
                                       profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeAgreement"


class LogisticsServiceCharge(Element):
    description = StringField(NS_FERD_1p0, "Description", required=True, profile=COMFORT,
                              _d="Identifikation der Servicegebühr")
    applied_amount = CurrencyField(NS_FERD_1p0, "AppliedAmount", required=True,
                                   profile=COMFORT, _d="Betrag der Servicegebühr")
    trade_tax = MultiField(ApplicableTradeTax, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedLogisticsServiceCharge"


class TradeSettlement(Element):
    payment_reference = StringField(NS_FERD_1p0, "PaymentReference")
    currency_code = StringField(NS_FERD_1p0, "InvoiceCurrencyCode")
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
    accounting_account = Field(AccountingAccount, required=False, profile=EXTENDED,
                               _d="Detailinformationen zur Buchungsreferenz")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeSettlement"


class TradeTransaction(Element):
    agreement = Field(TradeAgreement, required=True)
    delivery = Field(TradeDelivery, required=True)
    settlement = Field(TradeSettlement, required=True)
    items = MultiField(LineItem, required=True)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeTransaction"
