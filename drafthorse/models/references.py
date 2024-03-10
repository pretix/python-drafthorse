from . import BASIC, COMFORT, NS_RAM, NS_QDT
from .elements import Element
from .fields import BinaryObjectField, DateTimeField, StringField, IDField


class ProcuringProjectType(Element):
    id = StringField(NS_RAM, "ID")
    name = StringField(NS_RAM, "Name")

    class Meta:
        namespace = NS_RAM
        tag = "SpecifiedProcuringProject"


class ReferencedDocument(Element):
    issuer_assigned_id = IDField(
        NS_RAM, "IssuerAssignedID", required=False, profile=BASIC
    )
    issue_date_time = DateTimeField(
        NS_RAM,
        "FormattedIssueDateTime",
        required=True,
        profile=BASIC,
        date_time_namespace=NS_QDT,
    )


class SellerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "SellerOrderReferencedDocument"


class BuyerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "BuyerOrderReferencedDocument"


class ContractReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "ContractReferencedDocument"


class AdditionalReferencedDocument(ReferencedDocument):
    uri_id = StringField(NS_RAM, "URIID", required=False, profile=COMFORT)
    type_code = StringField(NS_RAM, "TypeCode", profile=COMFORT, required=True)
    name = StringField(NS_RAM, "Name", profile=COMFORT, required=False)
    attached_object = BinaryObjectField(
        NS_RAM, "AttachmentBinaryObject", required=False, profile=COMFORT
    )

    class Meta:
        namespace = NS_RAM
        tag = "AdditionalReferencedDocument"


class InvoiceReferencedDocument(ReferencedDocument):
    type_code = StringField(NS_RAM, "TypeCode", profile=COMFORT, required=False)

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
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "UltimateCustomerOrderReferencedDocument"


class LineBuyerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "BuyerOrderReferencedDocument"


class LineContractReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "ContractReferencedDocument"


class LineDespatchAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "DespatchAdviceReferencedDocument"


class LineReceivingAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "ReceivingAdviceReferencedDocument"


class LineAdditionalReferencedDocument(ReferencedDocument):
    uri_id = StringField(NS_RAM, "URIID", required=False, profile=COMFORT)
    line_id = StringField(NS_RAM, "LineID", required=False, profile=COMFORT)
    type_code = StringField(NS_RAM, "TypeCode", required=False, profile=COMFORT)
    name = StringField(NS_RAM, "Name", required=False, profile=COMFORT)
    reference_type_code = StringField(
        NS_RAM, "ReferenceTypeCode", profile=COMFORT, required=True
    )
    attached_object = BinaryObjectField(
        NS_RAM, "AttachmentBinaryObject", required=False, profile=COMFORT
    )

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
