import collections
import sys
import xml.etree.cElementTree as ET
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

from drafthorse.utils import validate_xml

from . import NS_UDT
from .container import Container
from .fields import Field


class BaseElementMeta(type):
    @classmethod
    def __prepare__(self, name, bases):
        return collections.OrderedDict()

    def __new__(mcls, name, bases, attrs):
        cls = super(BaseElementMeta, mcls).__new__(mcls, name, bases, attrs)
        fields = list(cls._fields) if hasattr(cls, '_fields') else []
        for attr, obj in attrs.items():
            if isinstance(obj, Field):
                if sys.version_info < (3, 6):
                    obj.__set_name__(cls, attr)
                fields.append(obj)
        cls._fields = fields
        return cls


class Element(metaclass=BaseElementMeta):
    def __init__(self, **kwargs):
        self.required = kwargs.get('required', False)
        self._data = OrderedDict([
            (f.name, f.initialize() if f.default else None) for f in self._fields
        ])
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _etree_node(self):
        node = ET.Element(self.get_tag())
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'attributes'):
            for k, v in self.Meta.attributes.items():
                node.set(k, v)
        return node

    def to_etree(self):
        node = self._etree_node()
        for k, v in self._data.items():
            if v is not None:
                v.append_to(node)
        return node

    def get_tag(self):
        return "{%s}%s" % (self.Meta.namespace, self.Meta.tag)

    def append_to(self, node):
        el = self.to_etree()
        if self.required or list(el) or el.text:
            node.append(el)

    def serialize(self):
        xml = b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + ET.tostring(self.to_etree(), "utf-8")
        return validate_xml(xmlout=xml, schema="ZUGFeRD1p0")

    def from_etree(self, root):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'namespace') and root.tag != "{%s}%s" % (
                self.Meta.namespace, self.Meta.tag):
            raise TypeError("Invalid XML, found tag {} where {} was expected".format(root.tag, "{%s}%s" % (
                self.Meta.namespace, self.Meta.tag)))
        field_index = {}
        for field in self._fields:
            element = getattr(self, field.name)
            field_index[element.get_tag()] = (field.name, element)
        for child in root:
            if child.tag == ET.Comment:
                continue
            if child.tag in field_index:
                name, childel = field_index[child.tag]
                if isinstance(getattr(self, name), Container):
                    getattr(self, name).add_from_etree(child)
                else:
                    getattr(self, name).from_etree(child)
            else:
                raise TypeError("Unknown element {}".format(child.tag))
        return self

    @classmethod
    def parse(cls, xmlinput):
        from lxml import etree
        root = etree.fromstring(xmlinput)
        return cls().from_etree(root)


class StringElement(Element):
    def __init__(self, namespace, tag, text=""):
        super().__init__()
        self.namespace = namespace
        self.tag = tag
        self.text = text

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, str(self))

    def __str__(self):
        return self.text

    def get_tag(self):
        return "{%s}%s" % (self.namespace, self.tag)

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        return node

    def from_etree(self, root):
        self.text = root.text
        return self


class DecimalElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self.value = value

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self.value) if self.value is not None else ""
        return node

    def __str__(self):
        return self.value

    def from_etree(self, root):
        self.value = Decimal(root.text)
        return self


class QuantityElement(StringElement):
    def __init__(self, namespace, tag, amount="", unit_code=""):
        super().__init__(namespace, tag)
        self.amount = amount
        self.unit_code = unit_code

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self.amount)
        node.attrib["unitCode"] = self.unit_code
        return node

    def __str__(self):
        return "{} {}".format(self.amount, self.unit_code)

    def from_etree(self, root):
        self.amount = Decimal(root.text)
        self.unit_code = root.attrib['unitCode']
        return self


class CurrencyElement(StringElement):
    def __init__(self, namespace, tag, amount="", currency="EUR"):
        super().__init__(namespace, tag)
        self.amount = amount
        self.currency = currency

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self.amount)
        node.attrib["currencyID"] = self.currency
        return node

    def from_etree(self, root):
        self.amount = Decimal(root.text)
        self.currency = root.attrib['currencyID']
        return self

    def __str__(self):
        return "{} {}".format(self.amount, self.currency)


class ClassificationElement(StringElement):
    def __init__(self, namespace, tag, text="", list_id="", list_version_id=""):
        super().__init__(namespace, tag)
        self.text = text
        self.list_id = list_id
        self.list_version_id = list_version_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        node.attrib['listID'] = self.list_id
        node.attrib['listVersionID'] = self.list_version_id
        return node

    def from_etree(self, root):
        self.text = Decimal(root.text)
        self.list_id = root.attrib['listID']
        self.list_version_id = root.attrib['listVersionID']
        return self

    def __str__(self):
        return "{} ({} {})".format(self.text, self.list_id, self.list_version_id)


class AgencyIDElement(StringElement):
    def __init__(self, namespace, tag, text="", scheme_id=""):
        super().__init__(namespace, tag)
        self.text = text
        self.scheme_id = scheme_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        node.attrib['schemeAgencyID'] = self.scheme_id
        return node

    def from_etree(self, root):
        self.text = root.text
        self.scheme_id = root.attrib['schemeAgencyID']
        return self

    def __str__(self):
        return "{} ({})".format(self.text, self.scheme_id)


class IDElement(StringElement):
    def __init__(self, namespace, tag, text="", scheme_id=""):
        super().__init__(namespace, tag)
        self.text = text
        self.scheme_id = scheme_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        node.attrib['schemeID'] = self.scheme_id
        return node

    def from_etree(self, root):
        self.text = root.text
        self.scheme_id = root.attrib['schemeID']
        return self

    def __str__(self):
        return "{} ({})".format(self.text, self.scheme_id)


class DateTimeElement(StringElement):
    def __init__(self, namespace, tag, value=None, format='102'):
        super().__init__(namespace, tag)
        self.value = value
        self.format = format

    def to_etree(self):
        t = self._etree_node()
        node = ET.Element("{%s}%s" % (NS_UDT, "DateTimeString"))
        if self.value:
            if self.format == '102':
                node.text = self.value.strftime("%Y%m%d")
            elif self.format == '616':
                if sys.version_info < (3, 6):
                    node.text = '{}{}'.format(self.value.isocalendar()[0], self.value.isocalendar()[1])
                else:
                    node.text = self.value.strftime("%G%V")
            node.attrib['format'] = self.format
            t.append(node)
        return t

    def from_etree(self, root):
        if len(root) != 1:
            raise TypeError("Date containers should have one child")
        if root[0].tag != "{%s}%s" % (NS_UDT, "DateTimeString"):
            raise TypeError("Tag %s not recognized" % root[0].tag)
        self.format = root[0].attrib['format']
        if self.format == '102':
            self.value = datetime.strptime(root[0].text, '%Y%m%d').date()
        elif self.format == '616':
            if sys.version_info < (3, 6):
                from isoweek import Week
                w = Week(int(root[0].text[:4]), int(root[0].text[4:]))
                self.value = w.monday()
            else:
                self.value = datetime.strptime(root[0].text + '1', '%G%V%u').date()
        else:
            raise TypeError("Date format %s cannot be parsed" % root[0].attrib['format'])
        return self

    def __str__(self):
        return "{}".format(self.value)


class DirectDateTimeElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self.value = value
        self.format = format

    def to_etree(self):
        t = self._etree_node()
        if self.value:
            t.text = self.value.strftime("%Y-%m-%dT%H:%M:%S")
        return t

    def from_etree(self, root):
        self.value = datetime.strptime(root.text, '%Y-%m-%dT%H:%M:%S').date()
        return self

    def __str__(self):
        return "{}".format(self.value)


class IndicatorElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self.value = value

    def get_tag(self):
        return "{%s}%s" % (self.namespace, self.tag)

    def to_etree(self):
        t = self._etree_node()
        if self.value is None:
            return t
        node = ET.Element("{%s}%s" % (NS_UDT, "Indicator"))
        node.text = str(self.value).lower()
        t.append(node)
        return t

    def __str__(self):
        return "{}".format(self.value)

    def from_etree(self, root):
        if len(root) != 1:
            raise TypeError("Indicator containers should have one child")
        if root[0].tag != "{%s}%s" % (NS_UDT, "Indicator"):
            raise TypeError("Tag %s not recognized" % root[0].tag)
        self.value = root[0].text == 'true'
        return self
