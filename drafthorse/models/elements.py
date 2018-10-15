import sys
import xml.etree.cElementTree as ET
from collections import OrderedDict

from drafthorse.utils import validate_xml
from . import NS_UDT
from .fields import Field


class BaseElementMeta(type):
    def __new__(mcls, name, bases, attrs):
        cls = super(BaseElementMeta, mcls).__new__(mcls, name, bases, attrs)
        fields = []
        for attr, obj in attrs.items():
            if isinstance(obj, Field):
                if sys.version_info < (3, 6):
                    obj.__set_name__(cls, attr)
                fields.append(obj)
        cls._fields = fields
        return cls


class Element(metaclass=BaseElementMeta):
    def __init__(self, **kwargs):
        self._data = OrderedDict([
            (f.name, f.initialize() if f.default else None) for f in self._fields
        ])
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _etree_node(self):
        node = ET.Element("{%s}%s" % (self.Meta.namespace, self.Meta.tag))
        if hasattr(self.Meta, 'attributes'):
            for k, v in self.Meta.attributes.items():
                node.set(k, v)
        return node

    def to_etree(self):
        node = self._etree_node()
        for v in self._data.values():
            if v is not None:
                v.append_to(node)
        return node

    def append_to(self, node):
        node.append(self.to_etree())

    def serialize(self):
        xml = b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + ET.tostring(self.to_etree(), "utf-8")
        print(xml)
        validate_xml(xmlout=xml, schema="ZUGFeRD1p0")
        return xml



class StringElement(Element):
    def __init__(self, namespace, tag, text=""):
        super().__init__()
        self.namespace = namespace
        self.tag = tag
        self.text = text

    def _etree_node(self):
        return ET.Element("{%s}%s" % (self.namespace, self.tag))

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        return node


class DecimalElement(StringElement):
    def __init__(self, namespace, tag, value=0):
        super().__init__(namespace, tag)
        self.value = value

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self.value)
        return node


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


class DateTimeElement(Element):
    def __init__(self, namespace, tag, value=None):
        super().__init__()
        self.value = None
        self.namespace = namespace
        self.tag = tag

    def to_etree(self):
        t = ET.Element("{%s}%s" % (self.namespace, self.tag))
        node = self._etree_node()
        node.text = self.value.strftime("%Y%m%d")
        t.append(node)
        return t

    class Meta:
        namespace = NS_UDT
        tag = "DateTimeString"
        attributes = {
            "format": "102"
        }


class IndicatorElement(Element):
    def __init__(self, namespace, tag, value=None):
        super().__init__()
        self.value = None
        self.namespace = namespace
        self.tag = tag

    def to_etree(self):
        t = ET.Element("{%s}%s" % (self.namespace, self.tag))
        node = self._etree_node()
        node.text = str(self.value).lower()
        t.append(node)
        return t

    class Meta:
        namespace = NS_UDT
        tag = "Indicator"
