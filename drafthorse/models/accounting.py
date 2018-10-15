from . import NS_FERD_1p0, COMFORT, EXTENDED, BASIC
from .elements import Element
from .fields import DateTimeField, StringField, CurrencyField, DecimalField, MultiField, IndicatorField


class LineApplicableTradeTax(Element):
    calculated_amount = CurrencyField(NS_FERD_1p0, "CalculatedAmount", required=True,
                                      profile=BASIC, _d="Steuerbetrag")
    type_code = StringField(NS_FERD_1p0, "TypeCode", required=True, profile=BASIC,
                            _d="Steuerart (Code)")
    exemption_reason = StringField(NS_FERD_1p0, "ExemptionReason", required=False,
                                   profile=COMFORT, _d="Grund der Steuerbefreiung (Freitext)")
    category_code = StringField(NS_FERD_1p0, "CategoryCode", required=False,
                                profile=COMFORT, _d="Steuerkategorie (Wert)")
    applicable_percent = DecimalField(NS_FERD_1p0, "ApplicablePercent",
                                      required=True, profile=BASIC)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ApplicableTradeTax"


class ApplicableTradeTax(LineApplicableTradeTax):
    basis_amount = CurrencyField(NS_FERD_1p0, "BasisAmount", required=True,
                                 profile=BASIC, _d="Basisbetrag der Steuerberechnung")
    line_total_basis_amount = CurrencyField(NS_FERD_1p0, "LineTotalBasisAmount",
                                            required=False, profile=EXTENDED,
                                            _d="Warenbetrag des Steuersatzes")
    allowance_charge_basis_amount = CurrencyField(NS_FERD_1p0, "AllowanceChargeBasisAmount",
                                                  required=False, profile=EXTENDED,
                                                  _d="Gesamtbetrag Zu- und Abschläge des Steuersatzes")


class AccountingAccount(Element):
    id = StringField(NS_FERD_1p0, "ID", required=True, profile=EXTENDED, _d="Buchungsreferenz")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ReceivableSpecifiedTradeAccount"


class MonetarySummation(Element):
    line_total = CurrencyField(NS_FERD_1p0, "LineTotalAmount", required=True,
                               profile=BASIC, _d="Gesamtbetrag der Positionen")
    charge_total = CurrencyField(NS_FERD_1p0, "ChargeTotalAmount", required=True,
                                 profile=BASIC, _d="Gesamtbetrag der Zuschläge")
    allowance_total = CurrencyField(NS_FERD_1p0, "AllowanceTotalAmount", required=True,
                                    profile=BASIC, _d="Gesamtbetrag der Abschläge")
    tax_basis_total = CurrencyField(NS_FERD_1p0, "TaxBasisTotalAmount", required=True,
                                    profile=BASIC, _d="Steuerbasisbetrag")
    tax_total = CurrencyField(NS_FERD_1p0, "TaxTotalAmount", required=True,
                              profile=BASIC, _d="Steuergesamtbetrag")
    grand_total = CurrencyField(NS_FERD_1p0, "GrandTotalAmount", required=True,
                                profile=BASIC, _d="Bruttosumme")
    prepaid_total = CurrencyField(NS_FERD_1p0, "TotalPrepaidAmount", required=False,
                                  profile=COMFORT, _d="Anzahlungsbetrag")
    due_amount = CurrencyField(NS_FERD_1p0, "DuePayableAmount", required=False,
                               profile=COMFORT, _d="Zahlbetrag")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementMonetarySummation"


class BillingSpecifiedPeriod(Element):
    start = DateTimeField(NS_FERD_1p0, "StartDateTime", required=True, profile=COMFORT)
    end = DateTimeField(NS_FERD_1p0, "EndDateTime", required=True, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "BillingSpecifiedPeriod"


class AppliedTradeTax(Element):
    type_code = StringField(NS_FERD_1p0, "TypeCode", required=True, profile=COMFORT)
    category_code = StringField(NS_FERD_1p0, "CategoryCode", required=True, profile=COMFORT)
    applicable_percent = StringField(NS_FERD_1p0, "ApplicablePercent", required=True, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AppliedTradeTax"


class CategoryTradeTax(AppliedTradeTax):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "CategoryTradeTax"


class TradeAllowanceCharge(Element):
    indicator = IndicatorField(NS_FERD_1p0, "ChargeIndicator", required=False, profile=COMFORT,
                               _d="Schalter für Zu-/Abschlag")
    sequence_numeric = DecimalField(NS_FERD_1p0, "SequenceNumeric", required=False, profile=EXTENDED,
                                    _d="Berechnungsreihenfolge")
    calculation_percent = DecimalField(NS_FERD_1p0, "CalculationPercent",
                                       required=False, profile=EXTENDED,
                                       _d="Rabatt in Prozent")
    basis_amount = CurrencyField(NS_FERD_1p0, "BasisAmount", required=False,
                                 profile=EXTENDED, _d="Basisbetrag des Rabatts")
    basis_quantity = CurrencyField(NS_FERD_1p0, "BasisQuantity", required=False,
                                   profile=EXTENDED, _d="Basismenge des Rabatts")
    actual_amount = CurrencyField(NS_FERD_1p0, "ActualAmount", required=True,
                                  profile=COMFORT, _d="Betrag des Zu-/Abschlags")
    reason_code = StringField(NS_FERD_1p0, "ReasonCode", required=False, profile=EXTENDED)
    reason = StringField(NS_FERD_1p0, "Reason", required=False, profile=COMFORT)
    trade_tax = MultiField(CategoryTradeTax, required=False, profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeAllowanceCharge"
