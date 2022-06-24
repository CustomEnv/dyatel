from dyatel.base.element import Element
from dyatel.base.group import Group


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


# Class variables


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


# Init variable


def test_base_group_selenium_set_parent_before_init_variable(mocked_selenium_driver):
    assert GroupChild().child_element_before_init_var.parent
    assert GroupChild().parent_element_before_init_var.parent


def test_base_group_appium_set_parent_before_init_variable(mocked_mobile_driver):
    assert GroupChild().child_element_before_init_var.parent
    assert GroupChild().parent_element_before_init_var.parent


def test_base_group_playwright_set_parent_before_init_variable(mocked_play_driver):
    assert GroupChild().child_element_before_init_var.parent
    assert GroupChild().parent_element_before_init_var.parent


def test_base_group_selenium_set_parent_after_init_variable(mocked_selenium_driver):
    assert GroupChild().child_element_after_init_var.parent
    assert GroupChild().parent_element_after_init_var.parent


def test_base_group_appium_set_parent_after_init_variable(mocked_mobile_driver):
    assert GroupChild().child_element_after_init_var.parent
    assert GroupChild().parent_element_after_init_var.parent


def test_base_group_playwright_set_parent_after_init_variable(mocked_play_driver):
    assert GroupChild().child_element_after_init_var.parent
    assert GroupChild().parent_element_after_init_var.parent
