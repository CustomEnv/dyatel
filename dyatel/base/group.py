from dyatel.base.element import Element
from dyatel.internal_utils import get_child_elements, AfterInitMeta


class Group(Element, metaclass=AfterInitMeta):

    def __init__(self, locator, locator_type=None, name=None):
        super(Group, self).__init__(locator, locator_type, name)

    def after_init(self):
        for element in get_child_elements(self, Element):
            element.parent = self
