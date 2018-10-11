class Field:
    def __init__(self, cls, default=False, required=False, _d=None):
        self.cls = cls
        self.required = required
        self.default = default
        self.__doc__ = _d
        super().__init__()

    def initialize(self):
        return self.cls()

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
    def __init__(self, namespace, tag, default=False, required=False, _d=None):
        from .elements import StringElement
        super().__init__(StringElement, default, required, _d)
        self.namespace = namespace
        self.tag = tag

    def initialize(self):
        return self.cls(self.namespace, self.tag)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].text = value


class DateTimeField(Field):
    def __init__(self, default=False, required=False, _d=None):
        from .elements import DateTimeElement
        super().__init__(DateTimeElement, default, required, _d)

    def __set__(self, instance, value):
        if instance._data.get(self.name, None) is None:
            instance._data[self.name] = self.initialize()
        instance._data[self.name].value = value


class Container():
    def __init__(self, child_type):
        super().__init__()
        self.children = []
        self.child_type = child_type

    def add(self, item):
        if not isinstance(item, self.child_type):
            raise TypeError("{} is not of type {}".format(item, self.child_type))
        self.children.append(item)

    def append_to(self, node):
        for child in self.children:
            child.append_to(node)


class MultiField(Field):
    def __init__(self, inner_type, default=False, required=False, _d=None):
        super().__init__(Container, default, required, _d)
        self.inner_type = inner_type

    def initialize(self):
        return self.cls(child_type=self.inner_type)
