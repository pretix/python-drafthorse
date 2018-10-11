import sys
import xml.etree.cElementTree as ET
from collections import OrderedDict

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
        return b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + ET.tostring(self.to_etree(), "utf-8")


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


class DateTimeElement(Element):
    def __init__(self, value=None):
        super().__init__()
        self.value = None

    def to_etree(self):
        node = self._etree_node()
        node.text = self.value.strftime("%Y%m%d")
        return node

    class Meta:
        namespace = NS_UDT
        tag = "DateTimeString"
        attributes = {
            "format": "102"
        }
