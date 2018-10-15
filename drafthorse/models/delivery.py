from . import BASIC, EXTENDED, NS_RAM
from .elements import Element
from .fields import DateTimeField, Field, IDField, StringField
from .party import (ShipFromTradeParty, ShipToTradeParty,
                    UltimateShipToTradeParty)
from .references import (DeliveryNoteReferencedDocument,
                         DespatchAdviceReferencedDocument)


class SupplyChainEvent(Element):
    occurrence = DateTimeField(NS_RAM, "OccurrenceDateTime",
                               required=False, profile=BASIC,
                               _d="Tatsächlicher Lieferungszeitpunkt")

    class Meta:
        namespace = NS_RAM
        tag = "ActualDeliverySupplyChainEvent"


class LogisticsTransportMovement(Element):
    mode_code = StringField(NS_RAM, "ModeCode", required=False, profile=EXTENDED)
    id = IDField(NS_RAM, "ID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLogisticsTransportMovement"


class SupplyChainConsignment(Element):
    movement = Field(LogisticsTransportMovement, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "RelatedSupplyChainConsignment"


class TradeDelivery(Element):
    consignment = Field(SupplyChainConsignment, default=False, required=False,
                        _d="Detailinformationen zur Konsignation oder Sendung")
    ship_to = Field(ShipToTradeParty, required=False, profile=EXTENDED)
    ultimate_ship_to = Field(UltimateShipToTradeParty, required=False, profile=EXTENDED)
    ship_from = Field(ShipFromTradeParty, required=False, profile=EXTENDED)
    event = Field(SupplyChainEvent, required=False, profile=BASIC)
    despatch_advice = Field(DespatchAdviceReferencedDocument, required=False,
                            profile=EXTENDED)
    delivery_note = Field(DeliveryNoteReferencedDocument, required=False,
                          profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableSupplyChainTradeDelivery"
