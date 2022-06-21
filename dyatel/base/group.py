from dyatel.base.element import Element


class Group(Element):

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        for element in self.child_elements:
            element.parent = self
