from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import (AgencyIDField, CurrencyField, DateTimeField, DecimalField,
                     Field, MultiCurrencyField, MultiStringField,
                     QuantityField, StringField)


class PayerFinancialAccount(Element):
    iban = StringField(NS_RAM, "IBANID")
    proprietary_id = StringField(NS_RAM, "ProprietaryID")

    class Meta:
        namespace = NS_RAM
        tag = "PayerPartyDebtorFinancialAccount"


class PayerFinancialInstitution(Element):
    bic = StringField(NS_RAM, "BICID")
    german_blz = StringField(NS_RAM, "GermanBankleitzahlID")
    name = StringField(NS_RAM, "Name")

    class Meta:
        namespace = NS_RAM
        tag = "PayerSpecifiedDebtorFinancialInstitution"


class PayeeFinancialAccount(Element):
    iban = StringField(NS_RAM, "IBANID")
    account_name = StringField(NS_RAM, "AccountName")
    proprietary_id = StringField(NS_RAM, "ProprietaryID")

    class Meta:
        namespace = NS_RAM
        tag = "PayeePartyCreditorFinancialAccount"


class PayeeFinancialInstitution(Element):
    bic = StringField(NS_RAM, "BICID")
    german_blz = StringField(NS_RAM, "GermanBankleitzahlID")
    name = StringField(NS_RAM, "Name")

    class Meta:
        namespace = NS_RAM
        tag = "PayeeSpecifiedCreditorFinancialInstitution"


class PaymentMeans(Element):
    type_code = StringField(NS_RAM, "TypeCode", required=False, profile=COMFORT)
    information = MultiStringField(NS_RAM, "Information", required=False, profile=COMFORT)
    id = AgencyIDField(NS_RAM, "ID", required=False, profile=BASIC)
    payer_account = Field(PayerFinancialAccount)
    payer_institution = Field(PayerFinancialInstitution)
    payee_account = Field(PayeeFinancialAccount)
    payee_institution = Field(PayeeFinancialInstitution)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeSettlementPaymentMeans"


class PaymentPenaltyTerms(Element):
    basis_date_time = DateTimeField(NS_RAM, "BasisDateTime", required=False,
                                    profile=EXTENDED, _d="Bezugsdatum der Fälligkeit")
    basis_period_measure = QuantityField(NS_RAM, "BasisPeriodMeasure", required=False,
                                         profile=EXTENDED, _d="Fälligkeitszeitraum")
    basis_amount = CurrencyField(NS_RAM, "BasisAmount", required=False,
                                 profile=EXTENDED, _d="Basisbetrag des Zahlungszuschlags")
    calculation_percent = DecimalField(NS_RAM, "CalculationPercent", required=False,
                                       profile=EXTENDED, _d="Prozentwert des Zahlungszuschlags")
    actual_amount = CurrencyField(NS_RAM, "ActualPenaltyAmount", required=False,
                                  profile=EXTENDED, _d="Betrag des Zahlungszuschlags")

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradePaymentPenaltyTerms"


class PaymentDiscountTerms(Element):
    basis_date_time = DateTimeField(NS_RAM, "BasisDateTime", required=False,
                                    profile=EXTENDED, _d="Bezugsdatum der Fälligkeit")
    basis_period_measure = QuantityField(NS_RAM, "BasisPeriodMeasure", required=False,
                                         profile=EXTENDED, _d="Fälligkeitszeitraum")
    basis_amount = CurrencyField(NS_RAM, "BasisAmount", required=False,
                                 profile=EXTENDED, _d="Basisbetrag des Zahlungsabschlags")
    calculation_percent = DecimalField(NS_RAM, "CalculationPercent", required=False,
                                       profile=EXTENDED, _d="Prozentwert des Zahlungsabschlags")
    actual_amount = CurrencyField(NS_RAM, "ActualDiscountAmount", required=False,
                                  profile=EXTENDED, _d="Betrag des Zahlungsabschlags")

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableTradePaymentDiscountTerms"


class PaymentTerms(Element):
    description = StringField(NS_RAM, "Description", required=True, profile=COMFORT,
                              _d="Freitext der Zahlungsbedingungen")
    due = DateTimeField(NS_RAM, "DueDateDateTime", required=False, profile=COMFORT,
                        _d="Fälligkeitsdatum")
    partial_amount = MultiCurrencyField(NS_RAM, "PartialPaymentAmount", profile=EXTENDED,
                                        required=False, _d="Betrag der Teilzahlung")
    penalty_terms = Field(PaymentPenaltyTerms, required=False, profile=EXTENDED,
                          _d="Detailinformationen zu Zahlungszuschlägen")
    discount_terms = Field(PaymentDiscountTerms, required=False, profile=EXTENDED,
                           _d="Detailinformationen zu Zahlungsabschlägen")

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradePaymentTerms"
