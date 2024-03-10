from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import (
    CurrencyField,
    DateTimeField,
    DecimalField,
    IndicatorField,
    MultiCurrencyField,
    MultiField,
    QuantityField,
    StringField,
)


class BillingSpecifiedPeriod(Element):
    description = StringField(
        NS_RAM,
        "Description",
        required=True,
        profile=COMFORT,
        _d="Freitext der Zahlungsbedingungen",
    )
    start = DateTimeField(NS_RAM, "StartDateTime", required=True, profile=COMFORT)
    end = DateTimeField(NS_RAM, "EndDateTime", required=True, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "BillingSpecifiedPeriod"


class ApplicableTradeTax(Element):
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
        profile=BASIC,
        _d="Grund der Steuerbefreiung (Freitext)",
    )
    basis_amount = DecimalField(
        NS_RAM,
        "BasisAmount",
        required=True,
        profile=BASIC,
        _d="Basisbetrag der Steuerberechnung",
    )
    line_total_basis_amount = DecimalField(
        NS_RAM,
        "LineTotalBasisAmount",
        required=False,
        profile=EXTENDED,
        _d="Warenbetrag des Steuersatzes",
    )
    allowance_charge_basis_amount = DecimalField(
        NS_RAM,
        "AllowanceChargeBasisAmount",
        required=False,
        profile=EXTENDED,
        _d="Gesamtbetrag Zu- und Abschläge des Steuersatzes",
    )
    category_code = StringField(
        NS_RAM,
        "CategoryCode",
        required=False,
        profile=BASIC,
        _d="Steuerkategorie (Wert)",
    )
    exemption_reason_code = StringField(
        NS_RAM,
        "ExemptionReasonCode",
        required=False,
        profile=BASIC,
        _d="Grund der Steuerbefreiung (Code)",
    )
    tax_point_date = DateTimeField(
        NS_RAM, "TaxPointDate", required=False, profile=COMFORT
    )
    due_date_type_code = StringField(
        NS_RAM,
        "DueDateTypeCode",
        required=False,
        profile=BASIC,
    )
    rate_applicable_percent = DecimalField(
        NS_RAM, "RateApplicablePercent", required=True, profile=BASIC
    )

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradeTax"


class AccountingAccount(Element):
    id = StringField(
        NS_RAM, "ID", required=True, profile=EXTENDED, _d="Buchungsreferenz"
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeAccountingAccount"


class ReceivableAccountingAccount(Element):
    id = StringField(
        NS_RAM, "ID", required=True, profile=EXTENDED, _d="Buchungsreferenz"
    )
    type_code = StringField(NS_RAM, "TypeCode", required=True, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "ReceivableSpecifiedTradeAccountingAccount"


class MonetarySummation(Element):
    line_total = DecimalField(
        NS_RAM,
        "LineTotalAmount",
        required=True,
        profile=BASIC,
        _d="Gesamtbetrag der Positionen",
    )
    charge_total = DecimalField(
        NS_RAM,
        "ChargeTotalAmount",
        required=True,
        profile=BASIC,
        _d="Gesamtbetrag der Zuschläge",
    )
    allowance_total = DecimalField(
        NS_RAM,
        "AllowanceTotalAmount",
        required=True,
        profile=BASIC,
        _d="Gesamtbetrag der Abschläge",
    )
    tax_basis_total = CurrencyField(
        NS_RAM,
        "TaxBasisTotalAmount",
        required=True,
        profile=BASIC,
        _d="Steuerbasisbetrag",
    )
    tax_total = CurrencyField(
        NS_RAM, "TaxTotalAmount", required=True, profile=BASIC, _d="Steuergesamtbetrag"
    )
    tax_total_other_currency = MultiCurrencyField(
        NS_RAM, "TaxTotalAmount", profile=EXTENDED, _d="Steuergesamtbetrag"
    )
    rounding_amount = DecimalField(
        NS_RAM,
        "RoundingAmount",
        required=False,
        profile=COMFORT,
    )
    grand_total = CurrencyField(
        NS_RAM, "GrandTotalAmount", required=True, profile=BASIC, _d="Bruttosumme"
    )
    prepaid_total = DecimalField(
        NS_RAM,
        "TotalPrepaidAmount",
        required=False,
        profile=COMFORT,
        _d="Anzahlungsbetrag",
    )
    due_amount = DecimalField(
        NS_RAM, "DuePayableAmount", required=False, profile=COMFORT, _d="Zahlbetrag"
    )

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeSettlementHeaderMonetarySummation"


class AppliedTradeTax(Element):
    type_code = StringField(NS_RAM, "TypeCode", required=True, profile=COMFORT)
    category_code = StringField(NS_RAM, "CategoryCode", required=True, profile=COMFORT)
    rate_applicable_percent = DecimalField(
        NS_RAM, "RateApplicablePercent", required=True, profile=COMFORT
    )

    class Meta:
        namespace = NS_RAM
        tag = "AppliedTradeTax"


class CategoryTradeTax(AppliedTradeTax):
    class Meta:
        namespace = NS_RAM
        tag = "CategoryTradeTax"


class TradeAllowanceCharge(Element):
    indicator = IndicatorField(
        NS_RAM,
        "ChargeIndicator",
        required=False,
        profile=COMFORT,
        _d="Schalter für Zu-/Abschlag",
    )
    sequence_numeric = DecimalField(
        NS_RAM,
        "SequenceNumeric",
        required=False,
        profile=EXTENDED,
        _d="Berechnungsreihenfolge",
    )
    calculation_percent = DecimalField(  # TODO: Should be deprecated?
        NS_RAM,
        "CalculationPercent",
        required=False,
        profile=COMFORT,
        _d="Rabatt in Prozent",
    )
    basis_amount = DecimalField(  # TODO: Should be deprecated?
        NS_RAM,
        "BasisAmount",
        required=False,
        profile=COMFORT,
        _d="Basisbetrag des Rabatts",
    )
    basis_quantity = QuantityField(
        NS_RAM,
        "BasisQuantity",
        required=False,
        profile=EXTENDED,
        _d="Basismenge des Rabatts",
    )
    actual_amount = DecimalField(
        NS_RAM,
        "ActualAmount",
        required=True,
        profile=COMFORT,
        _d="Betrag des Zu-/Abschlags",
    )
    reason_code = StringField(NS_RAM, "ReasonCode", required=False, profile=COMFORT)
    reason = StringField(NS_RAM, "Reason", required=False, profile=COMFORT)
    trade_tax = MultiField(CategoryTradeTax, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeAllowanceCharge"
