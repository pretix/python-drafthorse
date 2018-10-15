from . import NS_FERD_1p0, COMFORT, BASIC, EXTENDED
from .elements import Element
from .fields import StringField, Field, IDField, MultiField, MultiIDField


class PostalTradeAddress(Element):
    postcode = StringField(NS_FERD_1p0, "PostcodeCode", required=False, profile=BASIC)
    line_one = StringField(NS_FERD_1p0, "LineOne", required=False, profile=BASIC)
    line_two = StringField(NS_FERD_1p0, "LineTwo", required=False, profile=BASIC)
    city_name = StringField(NS_FERD_1p0, "CityName", required=False, profile=BASIC)
    country_id = StringField(NS_FERD_1p0, "CountryID", required=False, profile=BASIC)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "PostalTradeAddress"


class TaxRegistration(Element):
    id = IDField(NS_FERD_1p0, "ID")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedTaxRegistration"


class PhoneNumber(Element):
    number = StringField(NS_FERD_1p0, "CompleteNumber", required=False,
                         profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "TelephoneUniversalCommunication"


class FaxNumber(Element):
    number = StringField(NS_FERD_1p0, "CompleteNumber", required=False,
                         profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "FaxUniversalCommunication"


class EmailURI(Element):
    address = StringField(NS_FERD_1p0, "URIID", required=False,
                          profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "EmailURICommunication"


class TradeContact(Element):
    person_name = StringField(NS_FERD_1p0, "PersonName", required=False,
                              profile=EXTENDED)
    department_name = StringField(NS_FERD_1p0, "DepartmentName", required=False,
                                  profile=EXTENDED)
    telephone = Field(PhoneNumber, required=False, profile=EXTENDED)
    fax = Field(FaxNumber, required=False, profile=EXTENDED)
    email = Field(EmailURI, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "DefinedTradeContact"


class TradeParty(Element):
    id = StringField(NS_FERD_1p0, "ID", required=False, profile=COMFORT,
                     _d="Identifier des Verkäufers")
    global_id = MultiIDField(NS_FERD_1p0, "GlobalID", required=False, profile=COMFORT,
                             _d="Globaler Identifier des Verkäufers")
    name = StringField(NS_FERD_1p0, "Name", required=False, profile=BASIC)
    contact = Field(TradeContact, required=False, profile=EXTENDED,
                    _d="Ansprechpartner des Käufers")
    address = Field(PostalTradeAddress, required=False, profile=BASIC,
                    _d="Anschrift des Käufers")
    tax_registrations = MultiField(TaxRegistration, required=False, profile=BASIC)


class PayeeTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "PayeeTradeParty"


class InvoiceeTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "InvoiceeTradeParty"


class BuyerTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "BuyerTradeParty"


class SellerTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "SellerTradeParty"


class EndUserTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "ProductEndUserTradeParty"


class ShipToTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "ShipToTradeParty"


class ShipFromTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "ShipFromTradeParty"


class UltimateShipToTradeParty(TradeParty):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "UltimateShipToTradeParty"
