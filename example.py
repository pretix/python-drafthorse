from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from drafthorse.models.accounting import ApplicableTradeTax
from drafthorse.models.document import Document
from drafthorse.models.note import IncludedNote
from drafthorse.models.party import TaxRegistration
from drafthorse.models.payment import PaymentMeans, PaymentTerms
from drafthorse.models.trade import AdvancePayment, IncludedTradeTax
from drafthorse.models.tradelines import LineItem
from drafthorse.pdf import attach_xml

# Build data structure
doc = Document()
doc.context.guideline_parameter.id = "urn:cen.eu:en16931:2017"
doc.header.id = "RE1337"
doc.header.type_code = "380"
doc.header.issue_date_time = date.today()

doc.header.notes.add(IncludedNote(content="Test Note 1"))

doc.trade.agreement.buyer.name = "Kunde GmbH"
doc.trade.agreement.buyer.address.country_id = "DE"

doc.trade.settlement.currency_code = "EUR"
doc.trade.settlement.payment_means.add(PaymentMeans(type_code="ZZZ"))

doc.trade.agreement.seller.name = "Lieferant GmbH"
doc.trade.agreement.seller.address.country_id = "DE"
doc.trade.agreement.seller.address.country_subdivision = "Bayern"
doc.trade.agreement.seller.tax_registrations.add(
    TaxRegistration(
        id=("VA", "DE000000000")
    )
)

advance = AdvancePayment(
    received_date=datetime.now(timezone.utc), paid_amount=Decimal(42)
)
advance.included_trade_tax.add(
    IncludedTradeTax(
        calculated_amount=Decimal(0),
        type_code="VAT",
        category_code="E",
        rate_applicable_percent=Decimal(0),
    )
)
doc.trade.settlement.advance_payment.add(advance)

li = LineItem()
li.document.line_id = "1"
li.product.name = "Rainbow"
li.agreement.gross.amount = Decimal("1198.8")
li.agreement.gross.basis_quantity = (Decimal("1.0000"), "C62")  # C62 == unit
li.agreement.net.amount = Decimal("999")
li.agreement.net.basis_quantity = (Decimal("1.0000"), "C62")  # C62 == unit
li.delivery.billed_quantity = (Decimal("1.0000"), "C62")  # C62 == unit
li.settlement.trade_tax.type_code = "VAT"
li.settlement.trade_tax.category_code = "S"
li.settlement.trade_tax.rate_applicable_percent = Decimal("20.00")
li.settlement.monetary_summation.total_amount = Decimal("999.00")
doc.trade.items.add(li)

trade_tax = ApplicableTradeTax()
trade_tax.calculated_amount = Decimal("199.80")
trade_tax.basis_amount = Decimal("999.00")
trade_tax.type_code = "VAT"
trade_tax.category_code = "S"
trade_tax.rate_applicable_percent = Decimal("20.00")
doc.trade.settlement.trade_tax.add(trade_tax)

doc.trade.settlement.monetary_summation.line_total = Decimal("999.00")
doc.trade.settlement.monetary_summation.charge_total = Decimal("0.00")
doc.trade.settlement.monetary_summation.allowance_total = Decimal("0.00")
doc.trade.settlement.monetary_summation.tax_basis_total = Decimal("999.00")
doc.trade.settlement.monetary_summation.tax_total = (Decimal("199.80"), "EUR")
doc.trade.settlement.monetary_summation.grand_total = Decimal("1198.8")
doc.trade.settlement.monetary_summation.due_amount = Decimal("1198.8")

terms = PaymentTerms()
terms.due = datetime.now(timezone.utc) + timedelta(days=30)
doc.trade.settlement.terms.add(terms)

# Generate XML file
xml = doc.serialize(schema="FACTUR-X_EXTENDED")
