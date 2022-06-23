from dyatel.base.element import Element


class Group(Element):

    def __init__(self, locator, locator_type=None, name=None):
        super(Group, self).__init__(locator, locator_type, name)
        for element in self.child_elements:
            element.parent = self
