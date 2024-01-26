from . import BASIC, COMFORT, EXTENDED, NS_RAM, NS_RSM, NS_QDT
from .accounting import (
    ApplicableTradeTax,
    AppliedTradeTax,
    BillingSpecifiedPeriod,
    MonetarySummation,
    ReceivableAccountingAccount,
    TradeAllowanceCharge,
)
from .delivery import TradeDelivery
from .elements import Element
from .fields import DateTimeField, DecimalField, Field, MultiField, StringField
from .party import (
    BuyerTradeParty,
    EndUserTradeParty,
    InvoiceeTradeParty,
    InvoicerTradeParty,
    PayeeTradeParty,
    PayerTradeParty,
    SellerTaxRepresentativeTradeParty,
    SellerTradeParty,
)
from .payment import (
    PaymentMeans,
    PaymentTerms,
    TaxApplicableTradeCurrencyExchange,
)
from .references import (
    AdditionalReferencedDocument,
    BuyerOrderReferencedDocument,
    SellerOrderReferencedDocument,
    ContractReferencedDocument,
    InvoiceReferencedDocument,
    ProcuringProjectType,
    UltimateCustomerOrderReferencedDocument,
)
from .tradelines import LineItem


class DeliveryTerms(Element):
    type_code = StringField(
        NS_RAM,
        "DeliveryTypeCode",
        required=False,
        profile=EXTENDED,
        _d="Lieferbedingung (Code)",
    )

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradeDeliveryTerms"


class TradeAgreement(Element):
    buyer_reference = StringField(
        NS_RAM,
        "BuyerReference",
        required=False,
        profile=COMFORT,
        _d="Referenz des Käufers",
    )
    seller = Field(
        SellerTradeParty, required=True, _d="Detailinformationen zum Verkäufer"
    )
    buyer = Field(BuyerTradeParty, required=True)
    end_user = Field(
        EndUserTradeParty, required=False, _d="Abweichender Endverbraucher"
    )
    delivery_terms = Field(DeliveryTerms, required=False, profile=EXTENDED)
    seller_order = Field(SellerOrderReferencedDocument, required=False, profile=COMFORT)
    buyer_order = Field(BuyerOrderReferencedDocument, required=False)
    customer_order = Field(
        UltimateCustomerOrderReferencedDocument, required=False, profile=COMFORT
    )
    contract = Field(ContractReferencedDocument, required=False, profile=COMFORT)
    additional_references = MultiField(
        AdditionalReferencedDocument, required=False, profile=COMFORT
    )
    description = StringField(NS_RAM, "Description", required=False, profile=COMFORT)
    seller_tax_representative_party = Field(
        SellerTaxRepresentativeTradeParty, required=False
    )
    procuring_project_type = Field(ProcuringProjectType, required=False)

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableHeaderTradeAgreement"


class LogisticsServiceCharge(Element):
    description = StringField(
        NS_RAM,
        "Description",
        required=True,
        profile=COMFORT,
        _d="Identifikation der Servicegebühr",
    )
    applied_amount = DecimalField(
        NS_RAM,
        "AppliedAmount",
        required=True,
        profile=COMFORT,
        _d="Betrag der Servicegebühr",
    )
    trade_tax = MultiField(AppliedTradeTax, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLogisticsServiceCharge"


class IncludedTradeTax(Element):
    calculated_amount = DecimalField(
        NS_RAM, "CalculatedAmount", required=True, profile=BASIC, _d="Steuerbetrag"
    )
    type_code = StringField(
        NS_RAM, "TypeCode", required=True, profile=BASIC, _d="Steuerart (Code)"
    )
    exemption_reason = StringField(
        NS_RAM,
        "ExemptionReason",
        required=False,
        profile=COMFORT,
        _d="Grund der Steuerbefreiung (Freitext)",
    )
    exemption_reason_code = StringField(
        NS_RAM,
        "ExemptionReasonCode",
        required=False,
        profile=EXTENDED,
        _d="Grund der Steuerbefreiung (Code)",
    )
    category_code = StringField(
        NS_RAM,
        "CategoryCode",
        required=False,
        profile=COMFORT,
        _d="Steuerkategorie (Wert)",
    )
    rate_applicable_percent = DecimalField(
        NS_RAM, "RateApplicablePercent", required=True, profile=BASIC
    )

    class Meta:
        namespace = NS_RAM
        tag = "IncludedTradeTax"


class AdvancePayment(Element):
    paid_amount = DecimalField(NS_RAM, "PaidAmount")
    received_date = DateTimeField(
        NS_RAM, "FormattedReceivedDateTime", date_time_namespace=NS_QDT
    )
    included_trade_tax = MultiField(IncludedTradeTax)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedAdvancePayment"


class TradeSettlement(Element):
    creditor_reference_id = StringField(NS_RAM, "CreditorReferenceID")
    payment_reference = StringField(NS_RAM, "PaymentReference")
    tax_currency_code = StringField(
        NS_RAM, "TaxCurrencyCode", required=False, profile=BASIC
    )
    currency_code = StringField(NS_RAM, "InvoiceCurrencyCode")
    issuer_reference = StringField(NS_RAM, "InvoiceIssuerReference", profile=EXTENDED)
    invoicer = Field(
        InvoicerTradeParty, required=False, profile=EXTENDED, _d="Rechnungsaussteller"
    )
    invoicee = Field(
        InvoiceeTradeParty, required=False, profile=EXTENDED, _d="Rechnungsempfänger"
    )
    payee = Field(
        PayeeTradeParty, required=False, profile=BASIC, _d="Zahlungsempfänger"
    )
    payer = Field(
        PayerTradeParty, required=False, profile=EXTENDED, _d="Zahlungspflichtiger"
    )
    invoice_currency = Field(TaxApplicableTradeCurrencyExchange, profile=EXTENDED)
    payment_means = Field(PaymentMeans)
    trade_tax = MultiField(ApplicableTradeTax)
    period = Field(BillingSpecifiedPeriod, required=False, profile=BASIC)
    allowance_charge = MultiField(
        TradeAllowanceCharge,
        required=False,
        profile=BASIC,
        _d="Schalter für Zu-/Abschlag",
    )
    service_charge = MultiField(
        LogisticsServiceCharge, required=False, profile=EXTENDED
    )
    terms = MultiField(PaymentTerms, required=False, profile=BASIC)
    monetary_summation = Field(
        MonetarySummation,
        required=True,
        profile=BASIC,
        _d="Detailinformation zu Belegsummen",
    )
    invoice_referenced_document = Field(
        InvoiceReferencedDocument, required=False, profile=BASIC
    )
    accounting_account = Field(
        ReceivableAccountingAccount,
        required=False,
        profile=BASIC,
        _d="Detailinformationen zur Buchungsreferenz",
    )
    advance_payment = MultiField(AdvancePayment, required=False, profile=EXTENDED)

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
