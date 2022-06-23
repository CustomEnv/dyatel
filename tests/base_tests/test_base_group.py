from dyatel.base.element import Element
from dyatel.base.group import Group


class GroupParent(Group):
    def __init__(self):
        super(GroupParent, self).__init__(locator='sample', name='Parent Group')
        self.parent_element_init_var = Element('sample', name='parent element init var')

    parent_element_class_var = Element('sample', name='parent element class var')


class GroupChild(GroupParent):
    def __init__(self):
        self.child_element_init_var = Element('sample', name='child element init var')
        super(GroupChild, self).__init__()

    child_element_class_var = Element('sample', name='child element class var')


def test_base_group_selenium_set_parent_for_class_variable(mocked_selenium_driver):
    assert GroupChild().child_element_class_var.parent
    assert GroupChild().parent_element_class_var.parent
    assert GroupParent().parent_element_class_var.parent


def test_base_group_appium_set_parent_for_class_variable(mocked_mobile_driver):
    assert GroupChild().child_element_class_var.parent
    assert GroupChild().parent_element_class_var.parent
    assert GroupParent().parent_element_class_var.parent


def test_base_group_playwright_set_parent_for_class_variable(mocked_play_driver):
    assert GroupChild().child_element_class_var.parent
    assert GroupChild().parent_element_class_var.parent
    assert GroupParent().parent_element_class_var.parent


def test_base_group_selenium_set_parent_for_init_variable(mocked_selenium_driver):
    assert GroupChild().child_element_init_var.parent
    assert GroupChild().parent_element_init_var.parent
    assert GroupParent().parent_element_init_var.parent


def test_base_group_appium_set_parent_for_init_variable(mocked_mobile_driver):
    assert GroupChild().child_element_init_var.parent
    assert GroupChild().parent_element_init_var.parent
    assert GroupParent().parent_element_init_var.parent


def test_base_group_playwright_set_parent_for_init_variable(mocked_play_driver):
    assert GroupChild().child_element_init_var.parent
    assert GroupChild().parent_element_init_var.parent
    assert GroupParent().parent_element_init_var.parent
