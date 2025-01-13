from mops.base.element import Element
from mops.base.group import Group
from mops.base.page import Page


class SomePage(Page):
    def __init__(self):
        super(SomePage, self).__init__(locator='.somepage', name='Some page')


class GroupParent(Group):
    def __init__(self, name='Parent'):
        self.parent_element_before_init_var = Element('sample', name='parent element before init var')
        super(GroupParent, self).__init__(locator='sample', name=f'{name} Group')
        self.parent_element_after_init_var = Element('sample', name='parent element after init var')

    parent_element_class_var = Element('sample', name='parent element class var')


class GroupChild(GroupParent):
    def __init__(self):
        self.child_element_before_init_var = Element('sample', name='child element before init var')
        super(GroupChild, self).__init__(name='Child')
        self.child_element_after_init_var = Element('sample', name='child element after init var')

    child_element_class_var = Element('sample', name='child element class var')
