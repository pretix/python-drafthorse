from . import NS_FERD_1p0, EXTENDED, COMFORT
from .elements import Element
from .fields import StringField, QuantityField, IDField, MultiField, ClassificationField


class ProductCharacteristic(Element):
    type_code = StringField(NS_FERD_1p0, "TypeCode", required=True, profile=EXTENDED,
                            _d="Art der Produkteigenschaft")
    description = StringField(NS_FERD_1p0, "Description", required=True, profile=EXTENDED)
    value_measure = QuantityField(NS_FERD_1p0, "ValueMeasure", required=False,
                                  profile=EXTENDED, _d="Numerische Messgröße")
    value = StringField(NS_FERD_1p0, "Value", required=False, profile=EXTENDED)


class ProductClassification(Element):
    class_code = ClassificationField(NS_FERD_1p0, "ClassCode", required=True,
                                     profile=EXTENDED)
    value = StringField(NS_FERD_1p0, "ClassName", required=True, profile=EXTENDED)


class OriginCountry(Element):
    id = StringField(NS_FERD_1p0, "ID", required=True, profile=EXTENDED,
                     _d="Land der Produktherkunft")


class ReferencedProduct(Element):
    name = StringField(NS_FERD_1p0, "Name", required=False, profile=EXTENDED)
    description = StringField(NS_FERD_1p0, "Description", required=False, profile=EXTENDED)
    global_id = IDField(NS_FERD_1p0, "GlobalID", required=False, profile=EXTENDED)
    seller_assigned_id = StringField(NS_FERD_1p0, "SellerAssignedID", required=False,
                                     profile=EXTENDED)
    buyer_assigned_id = StringField(NS_FERD_1p0, "BuyerAssignedID", required=False,
                                    profile=EXTENDED)
    unit_quantity = QuantityField(NS_FERD_1p0, "UnitQuantity", required=False,
                                  profile=EXTENDED)


class TradeProduct(Element):
    name = StringField(NS_FERD_1p0, "Name", required=False, profile=COMFORT)
    description = StringField(NS_FERD_1p0, "Description", required=False, profile=COMFORT)
    global_id = IDField(NS_FERD_1p0, "GlobalID", required=False, profile=COMFORT)
    seller_assigned_id = StringField(NS_FERD_1p0, "SellerAssignedID", required=False,
                                     profile=COMFORT)
    buyer_assigned_id = StringField(NS_FERD_1p0, "BuyerAssignedID", required=False,
                                    profile=COMFORT)
    characteristics = MultiField(ProductCharacteristic, required=False, profile=EXTENDED)
    classifications = MultiField(ProductClassification, required=False, profile=EXTENDED)
    origins = MultiField(OriginCountry, required=False, profile=EXTENDED)
    included_products = MultiField(ReferencedProduct, required=False, profile=EXTENDED)
