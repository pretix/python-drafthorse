class Container:
    def __init__(self, child_type):
        super().__init__()
        self.children = []
        self.child_type = child_type

    def add(self, item):
        if isinstance(self.child_type, type) and not isinstance(item, self.child_type):
            raise TypeError("{} is not of type {}".format(item, self.child_type))
        self.children.append(item)

    def append_to(self, node):
        for child in self.children:
            child.append_to(node)

    def get_tag(self):
        return '{%s}%s' % (self.child_type.Meta.namespace, self.child_type.Meta.tag)

    def empty_element(self):
        return self.child_type()

    def add_from_etree(self, root):
        childel = self.empty_element()
        childel.from_etree(root)
        self.add(childel)


class SimpleContainer(Container):
    def __init__(self, child_type, namespace, tag):
        super().__init__(child_type)
        self.namespace = namespace
        self.tag = tag

    def get_tag(self):
        return '{%s}%s' % (self.namespace, self.tag)

    def empty_element(self):
        raise NotImplemented()

    def set_element(self, el, child):
        raise NotImplemented()

    def append_to(self, node):
        for child in self.children:
            el = self.empty_element()
            self.set_element(el, child)
            el.append_to(node)

    def add_from_etree(self, root):
        self.add(root.text)


class CurrencyContainer(SimpleContainer):

    def empty_element(self):
        from .elements import CurrencyElement
        return CurrencyElement(namespace=self.namespace, tag=self.tag)

    def set_element(self, el, child):
        el.amount = child[0]
        el.currency = child[1]

    def add_from_etree(self, root):
        self.add((root.text, root.attrib['currencyID']))


class IDContainer(SimpleContainer):
    def empty_element(self):
        from .elements import IDElement
        return IDElement(namespace=self.namespace, tag=self.tag)

    def set_element(self, el, child):
        el.text = child[1]
        el.scheme_id = child[0]

    def add_from_etree(self, root):
        self.add((root.attrib['schemeID'], root.text))


class StringContainer(SimpleContainer):

    def empty_element(self):
        from .elements import StringElement
        return StringElement(namespace=self.namespace, tag=self.tag)

    def set_element(self, el, child):
        el.text = child

    def add_from_etree(self, root):
        self.add(root.text)
