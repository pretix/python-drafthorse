from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import DateTimeField, Field, StringField
from .party import (
    ShipFromTradeParty,
    ShipToTradeParty,
    UltimateShipToTradeParty,
)
from .references import (
    DeliveryNoteReferencedDocument,
    DespatchAdviceReferencedDocument,
    ReceivingAdviceReferencedDocument,
)


class SupplyChainEvent(Element):
    occurrence = DateTimeField(
        NS_RAM,
        "OccurrenceDateTime",
        required=False,
        profile=BASIC,
        _d="Tatsächlicher Lieferungszeitpunkt",
    )

    class Meta:
        namespace = NS_RAM
        tag = "ActualDeliverySupplyChainEvent"


class LogisticsTransportMovement(Element):
    mode_code = StringField(NS_RAM, "ModeCode", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedLogisticsTransportMovement"


class SupplyChainConsignment(Element):  # TODO: Deprecated?
    movement: LogisticsTransportMovement = Field(
        LogisticsTransportMovement, required=False, profile=EXTENDED
    )

    class Meta:
        namespace = NS_RAM
        tag = "RelatedSupplyChainConsignment"


class TradeDelivery(Element):
    consignment: SupplyChainConsignment = Field(
        SupplyChainConsignment,
        default=False,
        required=False,
        profile=EXTENDED,
        _d="Detailinformationen zur Konsignation oder Sendung",
    )
    ship_to: ShipToTradeParty = Field(ShipToTradeParty, required=False, profile=COMFORT)
    ultimate_ship_to: UltimateShipToTradeParty = Field(
        UltimateShipToTradeParty, required=False, profile=EXTENDED
    )
    ship_from: ShipFromTradeParty = Field(
        ShipFromTradeParty, required=False, profile=EXTENDED
    )
    event: SupplyChainEvent = Field(SupplyChainEvent, required=False, profile=BASIC)
    despatch_advice: DespatchAdviceReferencedDocument = Field(
        DespatchAdviceReferencedDocument, required=False, profile=COMFORT
    )
    delivery_note: DeliveryNoteReferencedDocument = Field(
        DeliveryNoteReferencedDocument, required=False, profile=EXTENDED
    )
    receiving_advice: ReceivingAdviceReferencedDocument = Field(
        ReceivingAdviceReferencedDocument, required=False, profile=COMFORT
    )

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableHeaderTradeDelivery"
