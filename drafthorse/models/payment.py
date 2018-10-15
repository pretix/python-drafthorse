from . import NS_FERD_1p0, COMFORT, BASIC, EXTENDED
from .elements import Element
from .fields import Field, StringField, IDField, DateTimeField, DecimalField, CurrencyField, MultiStringField, \
    MultiCurrencyField


class PayerFinancialAccount(Element):
    iban = StringField(NS_FERD_1p0, "IBANID")
    proprietary_id = StringField(NS_FERD_1p0, "ProprietaryID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayerPartyDebtorFinancialAccount"


class PayerFinancialInstitution(Element):
    bic = StringField(NS_FERD_1p0, "BICID")
    german_blz = StringField(NS_FERD_1p0, "GermanBankleitzahlID")
    name = StringField(NS_FERD_1p0, "Name")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayerSpecifiedDebtorFinancialInstitution"


class PayeeFinancialAccount(Element):
    iban = StringField(NS_FERD_1p0, "IBANID")
    account_name = StringField(NS_FERD_1p0, "AccountName")
    proprietary_id = StringField(NS_FERD_1p0, "ProprietaryID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayeePartyCreditorFinancialAccount"


class PayeeFinancialInstitution(Element):
    bic = StringField(NS_FERD_1p0, "BICID")
    german_blz = StringField(NS_FERD_1p0, "GermanBankleitzahlID")
    name = StringField(NS_FERD_1p0, "Name")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayeeSpecifiedCreditorFinancialInstitution"


class PaymentMeans(Element):
    type_code = StringField(NS_FERD_1p0, "TypeCode", required=False, profile=COMFORT)
    information = MultiStringField(NS_FERD_1p0, "Information", required=False, profile=COMFORT)
    id = IDField(NS_FERD_1p0, "ID", required=False, profile=BASIC)
    payer_account = Field(PayerFinancialAccount)
    payer_institution = Field(PayerFinancialInstitution)
    payee_account = Field(PayeeFinancialAccount)
    payee_institution = Field(PayeeFinancialInstitution)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradeSettlementPaymentMeans"


class PaymentPenaltyTerms(Element):
    basis_date_time = DateTimeField(NS_FERD_1p0, "BasisDateTime", required=False,
                                    profile=EXTENDED, _d="Bezugsdatum der Fälligkeit")
    basis_period_measure = StringField(NS_FERD_1p0, "BasisPeriodMeasure", required=False,
                                       profile=EXTENDED, _d="Fälligkeitszeitraum")
    basis_amount = CurrencyField(NS_FERD_1p0, "BasisAmount", required=False,
                                 profile=EXTENDED, _d="Basisbetrag des Zahlungszuschlags")
    calculation_percent = DecimalField(NS_FERD_1p0, "CalculationPercent", required=False,
                                       profile=EXTENDED, _d="Prozentwert des Zahlungszuschlags")
    actual_amount = CurrencyField(NS_FERD_1p0, "ActualPenaltyAmount", required=False,
                                  profile=EXTENDED, _d="Betrag des Zahlungszuschlags")


class PaymentDiscountTerms(Element):
    basis_date_time = DateTimeField(NS_FERD_1p0, "BasisDateTime", required=False,
                                    profile=EXTENDED, _d="Bezugsdatum der Fälligkeit")
    basis_period_measure = StringField(NS_FERD_1p0, "BasisPeriodMeasure", required=False,
                                       profile=EXTENDED, _d="Fälligkeitszeitraum")
    basis_amount = CurrencyField(NS_FERD_1p0, "BasisAmount", required=False,
                                 profile=EXTENDED, _d="Basisbetrag des Zahlungsabschlags")
    calculation_percent = DecimalField(NS_FERD_1p0, "CalculationPercent", required=False,
                                       profile=EXTENDED, _d="Prozentwert des Zahlungsabschlags")
    actual_amount = CurrencyField(NS_FERD_1p0, "ActualDiscountAmount", required=False,
                                  profile=EXTENDED, _d="Betrag des Zahlungsabschlags")


class PaymentTerms(Element):
    description = StringField(NS_FERD_1p0, "Description", required=True, profile=COMFORT,
                              _d="Freitext der Zahlungsbedingungen")
    due = DateTimeField(NS_FERD_1p0, "DueDateDateTime", required=False, profile=COMFORT,
                        _d="Fälligkeitsdatum")
    partial_amount = MultiCurrencyField(NS_FERD_1p0, "PartialPaymentAmount", profile=EXTENDED,
                                        required=False, _d="Betrag der Teilzahlung")
    penalty_terms = Field(PaymentPenaltyTerms, required=False, profile=EXTENDED,
                          _d="Detailinformationen zu Zahlungszuschlägen")
    discount_terms = Field(PaymentDiscountTerms, required=False, profile=EXTENDED,
                           _d="Detailinformationen zu Zahlungsabschlägen")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTradePaymentTerms"
