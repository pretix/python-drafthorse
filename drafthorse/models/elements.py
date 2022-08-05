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
        fields = list(cls._fields) if hasattr(cls, "_fields") else []
        for attr, obj in attrs.items():
            if isinstance(obj, Field):
                if sys.version_info < (3, 6):
                    obj.__set_name__(cls, attr)
                fields.append(obj)
        cls._fields = fields
        return cls


class Element(metaclass=BaseElementMeta):
    def __init__(self, **kwargs):
        self.required = kwargs.get("required", False)
        self._data = OrderedDict(
            [
                (f.name, f.initialize() if f.default or f.required else None)
                for f in self._fields
            ]
        )
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _etree_node(self):
        node = ET.Element(self.get_tag())
        if hasattr(self, "Meta") and hasattr(self.Meta, "attributes"):
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

    def is_empty(self, el):
        return not list(el) and not el.text

    def append_to(self, node):
        el = self.to_etree()
        if self.required or not self.is_empty(el):
            node.append(el)

    def serialize(self, schema="FACTUR-X_BASIC"):
        xml = b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(
            self.to_etree(), "utf-8"
        )
        return validate_xml(xmlout=xml, schema=schema)

    def __setattr__(self, key, value):
        if (
            not hasattr(self, key)
            and not key.startswith("_")
            and not key in ("required",)
        ):
            raise AttributeError(
                f"Element {type(self)} has no attribute '{key}'. If you set it, it would not be included in the output."
            )
        return super().__setattr__(key, value)

    def from_etree(self, root):
        if (
            hasattr(self, "Meta")
            and hasattr(self.Meta, "namespace")
            and root.tag != "{%s}%s" % (self.Meta.namespace, self.Meta.tag)
        ):
            raise TypeError(
                "Invalid XML, found tag {} where {} was expected".format(
                    root.tag, "{%s}%s" % (self.Meta.namespace, self.Meta.tag)
                )
            )
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
        self._namespace = namespace
        self._tag = tag
        self._text = text
        self._set_on_input = False

    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, str(self))

    def __str__(self):
        return str(self.text)

    def is_empty(self, el):
        return super().is_empty(el) and not self._set_on_input

    def get_tag(self):
        return "{%s}%s" % (self._namespace, self._tag)

    def to_etree(self):
        node = self._etree_node()
        node.text = self._text
        return node

    def from_etree(self, root):
        self._text = root.text
        self._set_on_input = True
        return self


class DecimalElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self._value = value

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self._value) if self._value is not None else ""
        return node

    def __str__(self):
        return self.value

    def from_etree(self, root):
        self._value = Decimal(root.text)
        self._set_on_input = True
        return self


class QuantityElement(StringElement):
    def __init__(self, namespace, tag, amount="", unit_code=""):
        super().__init__(namespace, tag)
        self._amount = amount
        self._unit_code = unit_code

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self._amount)
        node.attrib["unitCode"] = self._unit_code
        return node

    def __str__(self):
        return "{} {}".format(self._amount, self._unit_code)

    def from_etree(self, root):
        self._amount = Decimal(root.text)
        self._unit_code = root.attrib["unitCode"]
        self._set_on_input = True
        return self


class CurrencyElement(StringElement):
    def __init__(self, namespace, tag, amount="", currency=None):
        super().__init__(namespace, tag)
        self._amount = amount
        self._currency = currency

    def to_etree(self):
        node = self._etree_node()
        node.text = str(self._amount)
        if self._currency is not None:
            node.attrib["currencyID"] = self._currency
        elif "currencyID" in node.attrib:
            del node.attrib["currencyID"]
        return node

    def from_etree(self, root):
        self._amount = Decimal(root.text)
        self._currency = root.attrib.get("currencyID") or None
        self._set_on_input = True
        return self

    def __str__(self):
        return "{} {}".format(self.amount, self.currency)


class ClassificationElement(StringElement):
    def __init__(self, namespace, tag, text="", list_id="", list_version_id=""):
        super().__init__(namespace, tag)
        self._text = text
        self._list_id = list_id
        self._list_version_id = list_version_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self.text
        node.attrib["listID"] = self._list_id
        node.attrib["listVersionID"] = self._list_version_id
        return node

    def from_etree(self, root):
        self._text = Decimal(root.text)
        self._list_id = root.attrib["listID"]
        self._list_version_id = root.attrib["listVersionID"]
        self._set_on_input = True
        return self

    def __str__(self):
        return "{} ({} {})".format(self._text, self._list_id, self._list_version_id)


class BinaryObjectElement(StringElement):
    def __init__(self, namespace, tag, text="", filename="", mime_code=""):
        super().__init__(namespace, tag)
        self._mime_code = mime_code
        self._filename = filename
        self._text = text

    def to_etree(self):
        node = self._etree_node()
        node.attrib["mimeCode"] = self._mime_code
        node.attrib["filename"] = self._filename
        node.text = self._text
        return node

    def from_etree(self, root):
        self._mime_code = root.attrib["mimeCode"]
        self._filename = root.attrib["filename"]
        self._text = root.text
        self._set_on_input = True
        return self

    def __str__(self):
        return "{} ({} {})".format(self._text, self._mime_code)


class AgencyIDElement(StringElement):
    def __init__(self, namespace, tag, text="", scheme_id=""):
        super().__init__(namespace, tag)
        self._text = text
        self._scheme_id = scheme_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self._text
        node.attrib["schemeAgencyID"] = self._scheme_id
        return node

    def from_etree(self, root):
        self._text = root.text
        self._scheme_id = root.attrib["schemeAgencyID"]
        self._set_on_input = True
        return self

    def __str__(self):
        return "{} ({})".format(self._text, self._scheme_id)


class IDElement(StringElement):
    def __init__(self, namespace, tag, text="", scheme_id=""):
        super().__init__(namespace, tag)
        self._text = text
        self._scheme_id = scheme_id

    def to_etree(self):
        node = self._etree_node()
        node.text = self._text
        node.attrib["schemeID"] = self._scheme_id
        return node

    def from_etree(self, root):
        self._text = root.text
        try:
            self._scheme_id = root.attrib["schemeID"]
        except:
            root.attrib["schemeID"] = ""
            self._scheme_id = root.attrib["schemeID"]
        self._set_on_input = True
        return self

    def __str__(self):
        return "{} ({})".format(self._text, self._scheme_id)


class DateTimeElement(StringElement):
    def __init__(self, namespace, tag, value=None, format="102"):
        super().__init__(namespace, tag)
        self._value = value
        self._format = format

    def to_etree(self):
        t = self._etree_node()
        node = ET.Element("{%s}%s" % (NS_UDT, "DateTimeString"))
        if self._value:
            if self._format == "102":
                node.text = self._value.strftime("%Y%m%d")
            elif self._format == "616":
                if sys.version_info < (3, 6):
                    node.text = "{}{}".format(
                        self._value.isocalendar()[0], self._value.isocalendar()[1]
                    )
                else:
                    node.text = self._value.strftime("%G%V")
            node.attrib["format"] = self._format
            t.append(node)
        return t

    def from_etree(self, root):
        if len(root) != 1:
            raise TypeError("Date containers should have one child")
        if root[0].tag != "{%s}%s" % (NS_UDT, "DateTimeString"):
            raise TypeError("Tag %s not recognized" % root[0].tag)
        self._format = root[0].attrib["format"]
        if self._format == "102":
            self._value = datetime.strptime(root[0].text, "%Y%m%d").date()
        elif self._format == "616":
            if sys.version_info < (3, 6):
                from isoweek import Week

                w = Week(int(root[0].text[:4]), int(root[0].text[4:]))
                self._value = w.monday()
            else:
                self._value = datetime.strptime(root[0].text + "1", "%G%V%u").date()
        else:
            raise TypeError(
                "Date format %s cannot be parsed" % root[0].attrib["format"]
            )
        self._set_on_input = True
        return self

    def __str__(self):
        return "{}".format(self._value)


class DirectDateTimeElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self._value = value

    def to_etree(self):
        t = self._etree_node()
        if self._value:
            t.text = self._value.strftime("%Y-%m-%dT%H:%M:%S")
        return t

    def from_etree(self, root):
        try:
            self._value = datetime.strptime(root.text, "%Y-%m-%dT%H:%M:%S").date()
        except:
            self._value = ""
        self._set_on_input = True
        return self

    def __str__(self):
        return "{}".format(self._value)


class IndicatorElement(StringElement):
    def __init__(self, namespace, tag, value=None):
        super().__init__(namespace, tag)
        self._value = value

    def get_tag(self):
        return "{%s}%s" % (self._namespace, self._tag)

    def to_etree(self):
        t = self._etree_node()
        if self._value is None:
            return t
        node = ET.Element("{%s}%s" % (NS_UDT, "Indicator"))
        node.text = str(self._value).lower()
        t.append(node)
        return t

    def __str__(self):
        return "{}".format(self._value)

    def from_etree(self, root):
        if len(root) != 1:
            raise TypeError("Indicator containers should have one child")
        if root[0].tag != "{%s}%s" % (NS_UDT, "Indicator"):
            raise TypeError("Tag %s not recognized" % root[0].tag)
        self._value = root[0].text == "true"
        self._set_on_input = True
        return self
