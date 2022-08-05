from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import (
    DateTimeField,
    DecimalField,
    Field,
    MultiCurrencyField,
    MultiStringField,
    QuantityField,
    StringField,
)


class FinancialCard(Element):
    id = StringField(NS_RAM, "ID")
    cardholder_name = StringField(NS_RAM, "CardholderName")

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradeSettlementFinancialCard"


class PayerFinancialAccount(Element):
    iban = StringField(NS_RAM, "IBANID")

    class Meta:
        namespace = NS_RAM
        tag = "PayerPartyDebtorFinancialAccount"


class PayeeFinancialAccount(Element):
    iban = StringField(NS_RAM, "IBANID")
    account_name = StringField(NS_RAM, "AccountName")
    proprietary_id = StringField(NS_RAM, "ProprietaryID")

    class Meta:
        namespace = NS_RAM
        tag = "PayeePartyCreditorFinancialAccount"


class PayeeFinancialInstitution(Element):
    bic = StringField(NS_RAM, "BICID")

    class Meta:
        namespace = NS_RAM
        tag = "PayeeSpecifiedCreditorFinancialInstitution"


class PaymentMeans(Element):
    type_code = StringField(NS_RAM, "TypeCode", required=True, profile=COMFORT)
    information = MultiStringField(
        NS_RAM, "Information", required=False, profile=COMFORT
    )
    financial_card = Field(FinancialCard)
    payer_account = Field(PayerFinancialAccount)
    payee_account = Field(PayeeFinancialAccount)
    payee_institution = Field(PayeeFinancialInstitution)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeSettlementPaymentMeans"


class PaymentPenaltyTerms(Element):
    basis_date_time = DateTimeField(
        NS_RAM,
        "BasisDateTime",
        required=False,
        profile=EXTENDED,
        _d="Bezugsdatum der Fälligkeit",
    )
    basis_period_measure = QuantityField(
        NS_RAM,
        "BasisPeriodMeasure",
        required=False,
        profile=EXTENDED,
        _d="Fälligkeitszeitraum",
    )
    basis_amount = DecimalField(
        NS_RAM,
        "BasisAmount",
        required=False,
        profile=EXTENDED,
        _d="Basisbetrag des Zahlungszuschlags",
    )
    calculation_percent = DecimalField(
        NS_RAM,
        "CalculationPercent",
        required=False,
        profile=EXTENDED,
        _d="Prozentwert des Zahlungszuschlags",
    )
    actual_amount = DecimalField(
        NS_RAM,
        "ActualPenaltyAmount",
        required=False,
        profile=EXTENDED,
        _d="Betrag des Zahlungszuschlags",
    )

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradePaymentPenaltyTerms"


class PaymentDiscountTerms(Element):
    basis_date_time = DateTimeField(
        NS_RAM,
        "BasisDateTime",
        required=False,
        profile=EXTENDED,
        _d="Bezugsdatum der Fälligkeit",
    )
    basis_period_measure = QuantityField(
        NS_RAM,
        "BasisPeriodMeasure",
        required=False,
        profile=EXTENDED,
        _d="Fälligkeitszeitraum",
    )
    basis_amount = DecimalField(
        NS_RAM,
        "BasisAmount",
        required=False,
        profile=EXTENDED,
        _d="Basisbetrag des Zahlungsabschlags",
    )
    calculation_percent = DecimalField(
        NS_RAM,
        "CalculationPercent",
        required=False,
        profile=EXTENDED,
        _d="Prozentwert des Zahlungsabschlags",
    )
    actual_amount = DecimalField(
        NS_RAM,
        "ActualDiscountAmount",
        required=False,
        profile=EXTENDED,
        _d="Betrag des Zahlungsabschlags",
    )

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradePaymentDiscountTerms"


class TaxApplicableTradeCurrencyExchange(Element):
    source_currency = StringField(
        NS_RAM, "SourceCurrencyCode", required=False, profile=EXTENDED
    )
    target_currency = StringField(
        NS_RAM, "TargetCurrencyCode", required=False, profile=EXTENDED
    )
    conversion_rate = DecimalField(
        NS_RAM, "ConversionRate", required=False, profile=EXTENDED
    )
    date_time_string = DateTimeField(
        NS_RAM, "ConversionRateDateTime", required=True, profile=EXTENDED
    )

    class Meta:
        namespace = NS_RAM
        tag = "TaxApplicableTradeCurrencyExchange"


class PaymentTerms(Element):
    description = StringField(
        NS_RAM,
        "Description",
        required=True,
        profile=COMFORT,
        _d="Freitext der Zahlungsbedingungen",
    )
    due = DateTimeField(
        NS_RAM,
        "DueDateDateTime",
        required=False,
        profile=COMFORT,
        _d="Fälligkeitsdatum",
    )
    debit_mandate_id = StringField(
        NS_RAM, "DirectDebitMandateID", required=False, profile=BASIC
    )
    partial_amount = MultiCurrencyField(
        NS_RAM,
        "PartialPaymentAmount",
        profile=EXTENDED,
        required=False,
        _d="Betrag der Teilzahlung",
    )
    penalty_terms = Field(
        PaymentPenaltyTerms,
        required=False,
        profile=EXTENDED,
        _d="Detailinformationen zu Zahlungszuschlägen",
    )
    discount_terms = Field(
        PaymentDiscountTerms,
        required=False,
        profile=EXTENDED,
        _d="Detailinformationen zu Zahlungsabschlägen",
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradePaymentTerms"
