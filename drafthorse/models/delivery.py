from . import NS_FERD_1p0, BASIC, EXTENDED
from .elements import Element
from .fields import DateTimeField, StringField, IDField, Field
from .party import ShipToTradeParty, ShipFromTradeParty, UltimateShipToTradeParty
from .references import DespatchAdviceReferencedDocument, DeliveryNoteReferencedDocument


class SupplyChainEvent(Element):
    occurrence = DateTimeField(NS_FERD_1p0, "OccurenceDateTime",
                               required=False, profile=BASIC,
                               _d="Tatsächlicher Lieferungszeitpunkt")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ActualDeliverySupplyChainEvent"


class LogisticsTransportMovement(Element):
    mode_code = StringField(NS_FERD_1p0, "ModeCode", required=False, profile=EXTENDED)
    id = IDField(NS_FERD_1p0, "ID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "SpecifiedLogisticsTransportMovement"


class SupplyChainConsignment(Element):
    movement = Field(LogisticsTransportMovement, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
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
        namespace = NS_FERD_1p0
        tag = "ApplicableSupplyChainTradeDelivery"
