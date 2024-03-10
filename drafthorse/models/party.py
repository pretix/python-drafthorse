from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import Field, IDField, MultiField, MultiIDField, StringField


class PostalTradeAddress(Element):
    postcode = StringField(NS_RAM, "PostcodeCode", required=False, profile=BASIC)
    line_one = StringField(NS_RAM, "LineOne", required=False, profile=BASIC)
    line_two = StringField(NS_RAM, "LineTwo", required=False, profile=BASIC)
    line_three = StringField(NS_RAM, "LineThree", required=False, profile=BASIC)
    city_name = StringField(NS_RAM, "CityName", required=False, profile=BASIC)
    country_id = StringField(NS_RAM, "CountryID", required=True, profile=BASIC)
    country_subdivision = StringField(
        NS_RAM, "CountrySubDivisionName", required=False, profile=BASIC
    )

    class Meta:
        namespace = NS_RAM
        tag = "PostalTradeAddress"


class URIUniversalCommunication(Element):
    uri_ID = IDField(NS_RAM, "URIID", required=False, profile=BASIC)

    class Meta:
        namespace = NS_RAM
        tag = "URIUniversalCommunication"


class TaxRegistration(Element):
    id = IDField(NS_RAM, "ID")

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTaxRegistration"


class PhoneNumber(Element):
    number = StringField(NS_RAM, "CompleteNumber", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "TelephoneUniversalCommunication"


class FaxNumber(Element):
    number = StringField(NS_RAM, "CompleteNumber", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "FaxUniversalCommunication"


class EmailURI(Element):
    address = StringField(NS_RAM, "URIID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "EmailURIUniversalCommunication"


class LegalOrganization(Element):
    id = IDField(NS_RAM, "ID", required=False, profile=BASIC)
    trade_name = StringField(
        NS_RAM,
        "TradingBusinessName",
        required=False,
        profile=BASIC,
        _d="Firmenname, sofern abweichend vom Namen",
    )
    trade_address = Field(PostalTradeAddress, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLegalOrganization"


class TradeContact(Element):
    person_name = StringField(NS_RAM, "PersonName", required=False, profile=EXTENDED)
    department_name = StringField(
        NS_RAM, "DepartmentName", required=False, profile=EXTENDED
    )
    telephone = Field(PhoneNumber, required=False, profile=EXTENDED)
    fax = Field(FaxNumber, required=False, profile=EXTENDED)
    email = Field(EmailURI, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "DefinedTradeContact"


class TradeParty(Element):
    id = StringField(
        NS_RAM, "ID", required=False, profile=COMFORT, _d="Kennung des Handelspartners"
    )
    global_id = MultiIDField(
        NS_RAM,
        "GlobalID",
        required=False,
        profile=COMFORT,
        _d="Globale Kennung des Handelspartners",
    )
    name = StringField(NS_RAM, "Name", required=False, profile=BASIC)
    description = StringField(
        NS_RAM,
        "Description",
        required=True,
        profile=COMFORT,
        _d="Zusätzliche rechliche Informationen des Handelspartners",
    )
    legal_organization = Field(
        LegalOrganization,
        required=False,
        profile=BASIC,
        _d="Handelsinformationen des Handelspartners",
    )
    contact = Field(
        TradeContact,
        required=False,
        profile=EXTENDED,
        _d="Ansprechpartner des Handelspartners",
    )
    address = Field(
        PostalTradeAddress,
        required=False,
        profile=BASIC,
        _d="Anschrift des Handelspartners",
    )
    electronic_address = MultiField(
        URIUniversalCommunication, required=False, profile=BASIC
    )
    tax_registrations = MultiField(TaxRegistration, required=False, profile=BASIC)


class SellerTaxRepresentativeTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "SellerTaxRepresentativeTradeParty"


class PayeeTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "PayeeTradeParty"


class PayerTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "PayerTradeParty"


class InvoicerTradeParty(TradeParty):
    class Meta:
        namespace = NS_RAM
        tag = "InvoicerTradeParty"


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
