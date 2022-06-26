from tests.adata.base import GroupChild, GroupParent


# Framework variables


def test_base_group_sel_framework_variables_access(mocked_selenium_driver):
    group = GroupChild()
    assert hasattr(group, 'driver')
    assert hasattr(group, 'driver_wrapper')
    assert hasattr(group, 'locator')
    assert hasattr(group, 'locator_type')
    assert hasattr(group, 'name')
    assert hasattr(group.child_element_class_var, 'parent')


def test_base_group_appium_framework_variables_access(mocked_mobile_driver):
    group = GroupChild()
    assert hasattr(group, 'driver')
    assert hasattr(group, 'driver_wrapper')
    assert hasattr(group, 'locator')
    assert hasattr(group, 'locator_type')
    assert hasattr(group, 'name')
    assert hasattr(group.child_element_class_var, 'parent')


def test_base_group_play_framework_variables_access(mocked_play_driver):
    group = GroupChild()
    parent_group = GroupParent()
    assert hasattr(group, 'driver')
    assert hasattr(group, 'driver_wrapper')
    assert hasattr(group, 'locator')
    assert hasattr(group, 'locator_type')
    assert hasattr(group, 'name')
    assert hasattr(group.child_element_class_var, 'parent')
    assert hasattr(parent_group, 'context')


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
