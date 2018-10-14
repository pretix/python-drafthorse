from drafthorse.models import NS_FERD_1p0
from drafthorse.models.elements import Element
from drafthorse.models.fields import StringField


class IncludedNote(Element):
    content = StringField(NS_FERD_1p0, "Content")
    subject_code = StringField(NS_FERD_1p0, "SubjectCode")

    class Meta:
        namespace = NS_FERD_1p0
        tag = "IncludedNote"
