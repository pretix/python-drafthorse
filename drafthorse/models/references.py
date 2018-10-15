from . import COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import DateTimeField, StringField


class ReferencedDocument(Element):
    issue_date_time = DateTimeField(NS_RAM, "IssueDateTime", required=False,
                                    profile=COMFORT)
    id = StringField(NS_RAM, "ID", required=False,
                     profile=COMFORT)


class BuyerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "BuyerOrderReferencedDocument"


class ContractReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "ContractReferencedDocument"


class AdditionalReferencedDocument(ReferencedDocument):
    type_code = StringField(NS_RAM, "ReferenceTypeCode", profile=EXTENDED, required=True)

    class Meta:
        namespace = NS_RAM
        tag = "AdditionalReferencedDocument"


class CustomerOrderReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "CustomerOrderReferencedDocument"


class DespatchAdviceReferencedDocument(ReferencedDocument):
    class Meta:
        namespace = NS_RAM
        tag = "DespatchAdviceReferencedDocument"


class LineCustomerOrderReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)

    class Meta:
        namespace = NS_RAM
        tag = "CustomerOrderReferencedDocument"


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


class LineAdditionalReferencedDocument(ReferencedDocument):
    line_id = StringField(NS_RAM, "LineID", required=False, profile=EXTENDED)
    type_code = StringField(NS_RAM, "ReferenceTypeCode", profile=EXTENDED, required=True)

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
        tag = "LineDeliveryNoteReferencedDocument"
