from . import NS_FERD_1p0, BASIC, COMFORT, EXTENDED
from .elements import Element
from .fields import StringField


class IncludedNote(Element):
    content = StringField(NS_FERD_1p0, "Content", required=False,
                          profile=BASIC)  # TODO: Can appear multiple times
    content_code = StringField(NS_FERD_1p0, "ContentCode", required=False,
                               profile=EXTENDED)
    subject_code = StringField(NS_FERD_1p0, "SubjectCode", required=False,
                               profile=COMFORT)

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IncludedNote"
