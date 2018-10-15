from . import BASIC, COMFORT, EXTENDED, NS_RAM
from .elements import Element
from .fields import MultiStringField, StringField


class IncludedNote(Element):
    content_code = StringField(NS_RAM, "ContentCode", required=False,
                               profile=EXTENDED)
    content = MultiStringField(NS_RAM, "Content", required=False,
                               profile=BASIC)
    subject_code = StringField(NS_RAM, "SubjectCode", required=False,
                               profile=COMFORT)

    class Meta:
        namespace = NS_RAM
        tag = "IncludedNote"
