from datetime import date

from drafthorse.models.document import Document, IncludedNote
from drafthorse.utils import prettify

doc = Document()
doc.context.parameter.id = "urn:ferd:CrossIndustryDocument:invoice:1p0:comfort"
doc.header.id = "RE1337"
doc.header.name = "RECHNUNG"
doc.header.type_code = "380"
doc.header.issue_date_time.value = date.today()
doc.header.notes.add(IncludedNote(content="Test Node 1"))
doc.header.notes.add(IncludedNote(content="Test Node 2"))
print(prettify(doc.serialize()))
