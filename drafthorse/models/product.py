from . import COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import (ClassificationField, IDField, MultiField, QuantityField,
                     StringField)


class ProductCharacteristic(Element):
    type_code = StringField(NS_RAM, "TypeCode", required=True, profile=EXTENDED,
                            _d="Art der Produkteigenschaft")
    description = StringField(NS_RAM, "Description", required=True, profile=EXTENDED)
    value_measure = QuantityField(NS_RAM, "ValueMeasure", required=False,
                                  profile=EXTENDED, _d="Numerische Messgröße")
    value = StringField(NS_RAM, "Value", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "ApplicableProductCharacteristic"


class ProductClassification(Element):
    class_code = ClassificationField(NS_RAM, "ClassCode", required=True,
                                     profile=EXTENDED)
    value = StringField(NS_RAM, "ClassName", required=True, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "DesignatedProductClassification"


class OriginCountry(Element):
    id = StringField(NS_RAM, "ID", required=True, profile=EXTENDED,
                     _d="Land der Produktherkunft")

    class Meta:
        namespace = NS_RAM
        tag = "OriginTradeCountry"


class ReferencedProduct(Element):
    global_id = IDField(NS_RAM, "GlobalID", required=False, profile=EXTENDED)
    seller_assigned_id = StringField(NS_RAM, "SellerAssignedID", required=False,
                                     profile=EXTENDED)
    buyer_assigned_id = StringField(NS_RAM, "BuyerAssignedID", required=False,
                                    profile=EXTENDED)
    name = StringField(NS_RAM, "Name", required=False, profile=EXTENDED)
    description = StringField(NS_RAM, "Description", required=False, profile=EXTENDED)
    unit_quantity = QuantityField(NS_RAM, "UnitQuantity", required=False,
                                  profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "IncludedReferencedProduct"


class TradeProduct(Element):
    global_id = IDField(NS_RAM, "GlobalID", required=False, profile=COMFORT)
    seller_assigned_id = StringField(NS_RAM, "SellerAssignedID", required=False,
                                     profile=COMFORT)
    buyer_assigned_id = StringField(NS_RAM, "BuyerAssignedID", required=False,
                                    profile=COMFORT)
    name = StringField(NS_RAM, "Name", required=False, profile=COMFORT)
    description = StringField(NS_RAM, "Description", required=False, profile=COMFORT)
    characteristics = MultiField(ProductCharacteristic, required=False, profile=EXTENDED)
    classifications = MultiField(ProductClassification, required=False, profile=EXTENDED)
    origins = MultiField(OriginCountry, required=False, profile=EXTENDED)
    included_products = MultiField(ReferencedProduct, required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedTradeProduct"
