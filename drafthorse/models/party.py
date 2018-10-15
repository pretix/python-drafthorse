from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import Field, IDField, MultiField, MultiIDField, StringField


class PostalTradeAddress(Element):
    postcode = StringField(NS_RAM, "PostcodeCode", required=False, profile=BASIC)
    line_one = StringField(NS_RAM, "LineOne", required=False, profile=BASIC)
    line_two = StringField(NS_RAM, "LineTwo", required=False, profile=BASIC)
    city_name = StringField(NS_RAM, "CityName", required=False, profile=BASIC)
    country_id = StringField(NS_RAM, "CountryID", required=False, profile=BASIC)

    class Meta:
        namespace = NS_RAM
        tag = "PostalTradeAddress"


class TaxRegistration(Element):
    id = IDField(NS_RAM, "ID")

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTaxRegistration"


class PhoneNumber(Element):
    number = StringField(NS_RAM, "CompleteNumber", required=False,
                         profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "TelephoneUniversalCommunication"


class FaxNumber(Element):
    number = StringField(NS_RAM, "CompleteNumber", required=False,
                         profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "FaxUniversalCommunication"


class EmailURI(Element):
    address = StringField(NS_RAM, "URIID", required=False,
                          profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "EmailURIUniversalCommunication"


class TradeContact(Element):
    person_name = StringField(NS_RAM, "PersonName", required=False,
                              profile=EXTENDED)
    department_name = StringField(NS_RAM, "DepartmentName", required=False,
                                  profile=EXTENDED)
    telephone = Field(PhoneNumber, required=False, profile=EXTENDED)
    fax = Field(FaxNumber, required=False, profile=EXTENDED)
    email = Field(EmailURI, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "DefinedTradeContact"


class TradeParty(Element):
    id = StringField(NS_RAM, "ID", required=False, profile=COMFORT,
                     _d="Identifier des Verkäufers")
    global_id = MultiIDField(NS_RAM, "GlobalID", required=False, profile=COMFORT,
                             _d="Globaler Identifier des Verkäufers")
    name = StringField(NS_RAM, "Name", required=False, profile=BASIC)
    contact = Field(TradeContact, required=False, profile=EXTENDED,
                    _d="Ansprechpartner des Käufers")
    address = Field(PostalTradeAddress, required=False, profile=BASIC,
                    _d="Anschrift des Käufers")
    tax_registrations = MultiField(TaxRegistration, required=False, profile=BASIC)


class PayeeTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "PayeeTradeParty"


class InvoiceeTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "InvoiceeTradeParty"


class BuyerTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "BuyerTradeParty"


class SellerTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "SellerTradeParty"


class EndUserTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "ProductEndUserTradeParty"


class ShipToTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "ShipToTradeParty"


class ShipFromTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "ShipFromTradeParty"


class UltimateShipToTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "UltimateShipToTradeParty"
