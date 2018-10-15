from datetime import date

from drafthorse.models.document import Document, IncludedNote
from drafthorse.utils import prettify

doc = Document()
doc.context.guideline_parameter.id = "urn:ferd:CrossIndustryDocument:invoice:1p0:comfort"
doc.header.id = "RE1337"
doc.header.name = "RECHNUNG"
doc.header.type_code = "380"
doc.header.issue_date_time.value = date.today()
doc.header.languages.add("de")
n = IncludedNote()
n.content.add("Test Node 1")
n.content.add("Test Node 2")
doc.header.notes.add(n)

doc.trade.agreement.seller.name = "Lieferant GmbH"

print(prettify(doc.serialize()))

samplexml = open("sample.xml", "rb").read()
doc = Document.parse(samplexml)

print(doc.header.name)
print(doc.trade.agreement.seller.name)
print([str(a.content) for a in doc.header.notes.children])