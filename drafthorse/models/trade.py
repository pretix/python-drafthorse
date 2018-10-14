from drafthorse.models.note import IncludedNote
from . import NS_RAM, NS_UDT, NS_FERD_1p0
from .elements import Element
from .fields import DateTimeField, Field, MultiField, StringField, IDField, CurrencyField, DecimalField, IndicatorField, \
    QuantityField


class PostalTradeAddress(Element):
    postcode = StringField(NS_FERD_1p0, "PostcodeCode")
    line_one = StringField(NS_FERD_1p0, "LineOne")
    city_name = StringField(NS_FERD_1p0, "CityName")
    country_id = StringField(NS_FERD_1p0, "CountryID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PostalTradeAddress"


class TaxRegistration(Element):
    id = IDField()

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTaxRegistration"


class BuyerTradeParty(Element):
    name = StringField(NS_FERD_1p0, "Name")
    address = Field(PostalTradeAddress)
    tax_registrations = MultiField(TaxRegistration)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "BuyerTradeParty"


class SellerTradeParty(Element):
    name = StringField(NS_FERD_1p0, "Name")
    address = Field(PostalTradeAddress)
    tax_registrations = MultiField(TaxRegistration)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SellerTradeParty"


class TradeAgreement(Element):
    seller = Field(SellerTradeParty)
    buyer = Field(BuyerTradeParty)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeAgreement"


class SupplyChainEvent(Element):
    occurrence = DateTimeField(NS_FERD_1p0, "OccurenceDateTime")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ActualDeliverySupplyChainEvent"


class TradeDelivery(Element):
    events = MultiField(SupplyChainEvent)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeDelivery"


class FinancialAccount(Element):
    iban = StringField(NS_FERD_1p0, "IBANID")
    account_name = StringField(NS_FERD_1p0, "AccountName")
    proprietary_id = StringField(NS_FERD_1p0, "ProprietaryID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayeePartyCreditorFinancialAccount"


class FinancialInstitution(Element):
    bic = StringField(NS_FERD_1p0, "BICID")
    german_blz = StringField(NS_FERD_1p0, "GermanBankleitzahlID")
    name = StringField(NS_FERD_1p0, "Name")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayeeSpecifiedCreditorFinancialInstitution"


class PaymentMeans(Element):
    type_code = StringField(NS_FERD_1p0, "TypeCode")
    information = StringField(NS_FERD_1p0, "Information")
    account = Field(FinancialAccount)
    institution = Field(FinancialInstitution)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementPaymentMeans"


class TradeTax(Element):
    calculated_amount = CurrencyField(NS_FERD_1p0, "CalculatedAmount", required=False)
    type_code = StringField(NS_FERD_1p0, "TypeCode")
    category_code = StringField(NS_FERD_1p0, "CategoryCode", required=False)
    basis_amount = CurrencyField(NS_FERD_1p0, "BasisAmount", required=False)
    applicable_percent = DecimalField(NS_FERD_1p0, "ApplicablePercent")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableTradeTax"


class PaymentTerms(Element):
    description = StringField(NS_FERD_1p0, "Description")
    due = DateTimeField(NS_FERD_1p0, "DueDateDateTime")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradePaymentTerms"


class MonetarySummation(Element):
    line_total = CurrencyField(NS_FERD_1p0, "LineTotalAmount")
    charge_total = CurrencyField(NS_FERD_1p0, "ChargeTotalAmount")
    allowance_total = CurrencyField(NS_FERD_1p0, "AllowanceTotalAmount")
    tax_basis_total = CurrencyField(NS_FERD_1p0, "TaxBasisTotalAmount")
    tax_total = CurrencyField(NS_FERD_1p0, "TaxTotalAmount")
    grand_total = CurrencyField(NS_FERD_1p0, "GrandTotalAmount")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementMonetarySummation"


class TradeSettlement(Element):
    payment_reference = StringField(NS_FERD_1p0, "PaymentReference")
    currency_code = StringField(NS_FERD_1p0, "InvoiceCurrencyCode")
    payment_means = Field(PaymentMeans)
    trade_tax = MultiField(TradeTax)
    terms = Field(PaymentTerms)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeSettlement"


class AllowanceCharge(Element):
    indicator = IndicatorField(NS_FERD_1p0, "ChargeIndicator")
    actual_amount = CurrencyField(NS_FERD_1p0, "ActualAmount")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AppliedTradeAllowanceCharge"


class GrossPrice(Element):
    amount = CurrencyField(NS_FERD_1p0, "ChargeAmount")
    charge = Field(AllowanceCharge)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "GrossPriceProductTradePrice"


class NetPrice(Element):
    amount = CurrencyField(NS_FERD_1p0, "ChargeAmount")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "NetPriceProductTradePrice"


class LineDocument(Element):
    gross = Field(GrossPrice)
    net = Field(NetPrice)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AssociatedDocumentLineDocument"


class LineAgreement(Element):
    line_id = StringField(NS_FERD_1p0, "LineID")
    note = Field(IncludedNote)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeAgreement"


class LineDelivery(Element):
    billed_quantity = QuantityField(NS_FERD_1p0, "BilledQuantity")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeDelivery"


class LineSummation(Element):
    total_amount = CurrencyField(NS_FERD_1p0, "LineTotalAmount")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementMonetarySummation"


class LineSettlement(Element):
    trade_tax = Field(TradeTax)
    monetary_summation = Field(LineSummation)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeSettlement"


class TradeProduct(Element):
    seller_assigned_id = StringField(NS_FERD_1p0, "SellerAssignedID")
    name = StringField(NS_FERD_1p0, "Name")


class LineItem(Element):
    document = Field(LineDocument)
    agreement = Field(LineAgreement)
    delivery = Field(LineDelivery)
    settlement = Field(LineSettlement)
    product = Field(TradeProduct)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IncludedSupplyChainTradeItem"


class TradeTransaction(Element):
    agreement = Field(TradeAgreement)
    delivery = Field(TradeDelivery)
    settlement = Field(TradeSettlement)
    items = MultiField(LineItem)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedSupplyChainTradeTransaction"
