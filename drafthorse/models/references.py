from . import COMFORT, EXTENDED, NS_FERD_1p0
from .elements import Element
from .fields import DateTimeField, StringField


class ReferencedDocument(Element):
    issue_date_time = DateTimeField(NS_FERD_1p0, "IssueDateTime", required=False,
                                    profile=COMFORT)
    id = StringField(NS_FERD_1p0, "ID", required=False,
                     profile=COMFORT)


class BuyerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "BuyerOrderReferencedDocument"


class ContractReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "ContractReferencedDocument"


class AdditionalReferencedDocument(ReferencedDocument):
    type_code = StringField(NS_FERD_1p0, "ReferenceTypeCode", profile=EXTENDED, required=True)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AdditionalReferencedDocument"


class CustomerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "CustomerOrderReferencedDocument"


class DespatchAdviceReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "DespatchAdviceReferencedDocument"


class LineCustomerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "CustomerOrderReferencedDocument"


class LineBuyerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "BuyerOrderReferencedDocument"


class LineContractReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ContractReferencedDocument"


class LineDespatchAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "DespatchAdviceReferencedDocument"


class LineReceivingAdviceReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "ReceivingAdviceReferencedDocument"


class LineAdditionalReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_FERD_1p0, "LineID", required=False, profile=EXTENDED)
    type_code = StringField(NS_FERD_1p0, "ReferenceTypeCode", profile=EXTENDED, required=True)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "AdditionalReferencedDocument"


class DeliveryNoteReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "DeliveryNoteReferencedDocument"


class LineDeliveryNoteReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_FERD_1p0
        tag = "LineDeliveryNoteReferencedDocument"
