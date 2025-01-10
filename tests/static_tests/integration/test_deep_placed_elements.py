from mops.base.element import Element
from mops.base.group import Group


class GroupMain(Group):
    def __init__(self, locator='main_locator', name='main group'):
        super().__init__(locator, name=name)

    some_element = Element('main_element', name='main element')
    some_child_element = Element('child_element', name='child element', parent=some_element)


class GroupChild1(GroupMain):
    def __init__(self):
        super().__init__('group_child_1', name='group child 1')


class GroupChild2(GroupMain):
    def __init__(self):
        super().__init__('group_child_2', name='group child 2')


class Group2(GroupChild1):
    pass


class Group3(Group2):
    pass


def test_deep_placed_element_init(mocked_selenium_driver):
    assert hasattr(Group3().some_element, '_element')


def test_deep_placed_element_with_parent(mocked_selenium_driver):
    assert GroupChild1().some_child_element != GroupChild1().some_child_element
    assert GroupChild1().some_child_element.parent
    assert GroupChild2().some_child_element.parent
