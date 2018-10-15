from . import BASIC
from .container import (Container, CurrencyContainer, IDContainer,
                        StringContainer)


class Field:
    def __init__(self, cls, default=False, required=False, profile=BASIC, _d=None):
        self.cls = cls
        self.required = required
        self.default = default
        self.__doc__ = _d
        self.profile = profile
        super().__init__()

    def initialize(self):
        return self.cls(required=self.required)

    def __get__(self, instance, objtype):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        return instance._data[self.name]

    def __set__(self, instance, value):
        raise AttributeError("Read-only!")

    def __delete__(self, instance):
        del instance._data[self.name]

    def __set_name__(self, owner, name):
        self.name = name


class StringField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import StringElement
        super().__init__(StringElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].text = value


class AgencyIDField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import AgencyIDElement
        super().__init__(AgencyIDElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()

        if not isinstance(value, (tuple, list)):
            raise TypeError("Please pass a 2-tuple of scheme agency ID and ID.")
        instance._data[self.name].text = value[1]
        instance._data[self.name].scheme_id = value[0]


class ClassificationField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import ClassificationElement
        super().__init__(ClassificationElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()

        if not isinstance(value, (tuple, list)):
            raise TypeError("Please pass a 3-tuple of list ID, list version and ID.")
        instance._data[self.name].text = value[2]
        instance._data[self.name].list_id = value[0]
        instance._data[self.name].list_version_id = value[1]


class IDField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import IDElement
        super().__init__(IDElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()

        if not isinstance(value, (tuple, list)):
            raise TypeError("Please pass a 2-tuple of including scheme ID and ID.")
        instance._data[self.name].text = value[1]
        instance._data[self.name].scheme_id = value[0]


class DecimalField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import DecimalElement
        super().__init__(DecimalElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class QuantityField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import QuantityElement
        super().__init__(QuantityElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()

        if not isinstance(value, (tuple, list)):
            raise TypeError("Please pass a 2-tuple of including amount and unit code.")
        instance._data[self.name].value = value[0]
        instance._data[self.name].unit_code = value[1]

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class CurrencyField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import CurrencyElement
        super().__init__(CurrencyElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()

        if not isinstance(value, (tuple, list)):
            raise TypeError("Please pass a 2-tuple of including amount and currency.")
        instance._data[self.name].value = value[0]
        instance._data[self.name].currency = value[1]

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class IndicatorField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import IndicatorElement
        super().__init__(IndicatorElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].value = value

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class DateTimeField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import DateTimeElement
        super().__init__(DateTimeElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].value = value

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class DirectDateTimeField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        from .elements import DirectDateTimeElement
        super().__init__(DirectDateTimeElement, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].value = value

    def initialize(self):
        return self.cls(self.namespace, self.tag)


class MultiField(Field):
    def __init__(self, inner_type, default=False, required=False, profile=BASIC, _d=None):
        super().__init__(Container, default, required, profile, _d)
        self.inner_type = inner_type

    def initialize(self):
        return self.cls(child_type=self.inner_type)


class MultiStringField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        super().__init__(StringContainer, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(child_type=str, namespace=self.namespace, tag=self.tag)


class MultiCurrencyField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        super().__init__(CurrencyContainer, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(child_type=(tuple, list), namespace=self.namespace, tag=self.tag)


class MultiIDField(Field):
    def __init__(self, namespace, tag, default=False, required=False, profile=BASIC, _d=None):
        super().__init__(IDContainer, default, required, profile, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(child_type=(tuple, list), namespace=self.namespace, tag=self.tag)
