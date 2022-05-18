from . import BASIC, COMFORT, EXTENDED, NS_RAM, NS_RSM
from .accounting import (
    ApplicableTradeTax, AppliedTradeTax,
    MonetarySummation, ReceivableAccountingAccount, TradeAllowanceCharge, BillingSpecifiedPeriod, SellerOrderReferencedDocument
)
from .delivery import TradeDelivery
from .elements import Element
from .fields import DecimalField, Field, MultiField, StringField, IDField
from .party import (
    BuyerTradeParty, EndUserTradeParty, InvoiceeTradeParty, PayeeTradeParty,
    SellerTradeParty, SellerTaxRepresentativeTradeParty,
)
from .payment import PaymentMeans, PaymentTerms
from .references import (
    AdditionalReferencedDocument, BuyerOrderReferencedDocument,
    ContractReferencedDocument, UltimateCustomerOrderReferencedDocument, ProcuringProjectType, InvoiceReferencedDocument
)
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
    customer_order = Field(UltimateCustomerOrderReferencedDocument, required=False, profile=COMFORT)
    contract = Field(ContractReferencedDocument, required=False, profile=COMFORT)
    additional_references = MultiField(AdditionalReferencedDocument, required=False,
                                       profile=COMFORT)
    description = StringField(NS_RAM, "Description", required=False,
                                  profile=COMFORT)
    seller_tax_representative_party = Field(SellerTaxRepresentativeTradeParty, required=False)
    order_document = Field(SellerOrderReferencedDocument, required=False)
    procuring_project_type = Field(ProcuringProjectType, required=False)
    class Meta:
        namespace = NS_RAM
        tag = "ApplicableHeaderTradeAgreement"


class LogisticsServiceCharge(Element):
    description = StringField(NS_RAM, "Description", required=True, profile=COMFORT,
                              _d="Identifikation der Servicegebühr")
    applied_amount = DecimalField(NS_RAM, "AppliedAmount", required=True,
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
    allowance_charge = MultiField(TradeAllowanceCharge, required=False, profile=COMFORT,
                                  _d="Schalter für Zu-/Abschlag")
    service_charge = MultiField(LogisticsServiceCharge, required=False, profile=COMFORT)
    terms = MultiField(PaymentTerms, required=False, profile=COMFORT)
    monetary_summation = Field(MonetarySummation, required=True, profile=BASIC,
                               _d="Detailinformation zu Belegsummen")
    accounting_account = Field(ReceivableAccountingAccount, required=False, profile=EXTENDED,
                               _d="Detailinformationen zur Buchungsreferenz")
    creditor_reference_ID = IDField(NS_RAM, "CreditorReferenceID")
    period = Field(BillingSpecifiedPeriod, required=False, profile=BASIC)
    tax_currency_code = StringField(NS_RAM, "TaxCurrencyCode", required=False, profile=COMFORT)
    invoice_referenced_document = Field(InvoiceReferencedDocument, required=False, profile=BASIC)
    class Meta:
        namespace = NS_RAM
        tag = "ApplicableHeaderTradeSettlement"


class TradeTransaction(Element):
    items = MultiField(LineItem, required=True)
    agreement = Field(TradeAgreement, required=True)
    delivery = Field(TradeDelivery, required=True)
    settlement = Field(TradeSettlement, required=True)

    class Meta:
        namespace = NS_RSM
        tag = "SupplyChainTradeTransaction"
