from . import COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import DirectDateTimeField, StringField, Field

class ProcuringProjectType(Element):
    id = StringField(NS_RAM, "ID")
    name = StringField(NS_RAM, "Name")
    class Meta:
        namespace = NS_RAM
        tag = "ProcuringProjectType"

class ReferencedDocument(Element):
    date_time_string = DirectDateTimeField(NS_RAM, "DateTimeString", required=False,
                                           profile=COMFORT)
    issuer_assigned_id = StringField(NS_RAM, "IssuerAssignedID", required=False,
                                     profile=COMFORT)
class AttachmentBinaryObject(Element):
    name = StringField(NS_RAM, "filename", profile=EXTENDED)
    class Meta:
        namespace = NS_RAM
        tag = "AttachmentBinaryObject"

class BuyerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "BuyerOrderReferencedDocument"


class ContractReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "ContractReferencedDocument"


class AdditionalReferencedDocument(Element):
    issuer_assigned_id = StringField(NS_RAM, "IssuerAssignedID", required=False,
                                     profile=COMFORT)
    uri_id = StringField(NS_RAM, "URIID", required=False,
                                     profile=EXTENDED)
    date_time_string = DirectDateTimeField(NS_RAM, "DateTimeString", required=False,
                                           profile=COMFORT)
    type_code = StringField(NS_RAM, "TypeCode", profile=EXTENDED, required=True)
    name = StringField(NS_RAM, "Name", profile=COMFORT, required=False)
    attached_object = Field(AttachmentBinaryObject, required=False, profile=EXTENDED)
    class Meta:
        namespace = NS_RAM
        tag = "AdditionalReferencedDocument"

class InvoiceReferencedDocument(Element):
    issuer_assigned_id = StringField(NS_RAM, "IssuerAssignedID", required=False,
                                     profile=COMFORT)

    date_time_string = DirectDateTimeField(NS_RAM, "DateTimeString", required=True,
                                           profile=COMFORT)
    type_code = StringField(NS_RAM, "TypeCode", profile=EXTENDED, required=False)


    class Meta:
        namespace = NS_RAM
        tag = "InvoiceReferencedDocument"


class UltimateCustomerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "UltimateCustomerOrderReferencedDocument"


class DespatchAdviceReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "DespatchAdviceReferencedDocument"


class LineUltimateCustomerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "UltimateCustomerOrderReferencedDocument"


class LineBuyerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "BuyerOrderReferencedDocument"


class LineContractReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "ContractReferencedDocument"


class LineDespatchAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "DespatchAdviceReferencedDocument"


class LineReceivingAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "ReceivingAdviceReferencedDocument"


class LineAdditionalReferencedDocument(Element):
    issuer_assigned_id = StringField(NS_RAM, "IssuerAssignedID", required=False,
                                     profile=COMFORT)
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)
    date_time_string = DirectDateTimeField(NS_RAM, "DateTimeString", required=False,
                                           profile=COMFORT)
    reference_type_code = StringField(NS_RAM, "ReferenceTypeCode", profile=EXTENDED, required=True)

    class Meta:
        namespace = NS_RAM
        tag = "AdditionalReferencedDocument"


class DeliveryNoteReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "DeliveryNoteReferencedDocument"


class LineDeliveryNoteReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "DeliveryNoteReferencedDocument"
