import pytest

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page
from tests.static_tests.conftest import mobile_drivers, mobile_ids


class MyGroup(Group):
    repr_element = Element('element-repr')


def test_ios_and_desktop_driver_repr(mocked_ios_driver, mocked_selenium_driver):
    ios_info = repr(mocked_ios_driver)
    desktop_info = repr(mocked_selenium_driver)
    assert 'platform=ios' in ios_info
    assert '1_driver' in ios_info
    assert 'DriverWrapper' in ios_info
    assert 'at 0x' in ios_info
    assert 'appium.webdriver.webdriver.WebDriver' in ios_info

    assert 'platform=desktop' in desktop_info
    assert '2_driver' in desktop_info
    assert 'ShadowDriverWrapper' in desktop_info
    assert 'at 0x' in desktop_info
    assert 'selenium.webdriver' in desktop_info


def test_android_and_desktop_driver_repr(mocked_android_driver, mocked_selenium_driver):
    android_info = repr(mocked_android_driver)
    desktop_info = repr(mocked_selenium_driver)
    assert 'platform=android' in android_info
    assert '1_driver' in android_info
    assert 'DriverWrapper' in android_info
    assert 'at 0x' in android_info
    assert 'appium.webdriver.webdriver.WebDriver' in android_info

    assert 'platform=desktop' in desktop_info
    assert '2_driver' in desktop_info
    assert 'ShadowDriverWrapper' in desktop_info
    assert 'at 0x' in desktop_info
    assert 'selenium.webdriver' in desktop_info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_mobile_and_desktop_element_repr(driver, request):
    mobile_driver = request.getfixturevalue(driver)
    desktop_driver = request.getfixturevalue('mocked_selenium_driver')
    mobile_group = MyGroup('repr-group', driver_wrapper=mobile_driver)
    desktop_group = MyGroup('repr-group', driver_wrapper=desktop_driver)
    mobile_info = repr(mobile_group.repr_element)
    desktop_info = repr(desktop_group.repr_element)

    assert 'Element' in mobile_info
    assert 'locator="[id="element-repr"]"' in mobile_info
    assert 'locator_type="css selector"' in mobile_info
    assert 'name="element-repr"' in mobile_info
    assert 'parent=MyGroup' in mobile_info
    assert 'at 0x' in mobile_info
    assert '1_driver' in mobile_info
    assert 'appium.webdriver.webdriver.WebDriver' in mobile_info

    assert 'Element' in desktop_info
    assert 'locator="element-repr"' in desktop_info
    assert 'locator_type="id"' in desktop_info
    assert 'name="element-repr"' in desktop_info
    assert 'parent=MyGroup' in desktop_info
    assert 'at 0x' in desktop_info
    assert '2_driver' in desktop_info
    assert 'selenium.webdriver' in desktop_info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_mobile_and_desktop_group_repr(driver, request):
    mobile_driver = request.getfixturevalue(driver)
    desktop_driver = request.getfixturevalue('mocked_selenium_driver')
    mobile_group = MyGroup('repr-group', driver_wrapper=mobile_driver)
    desktop_group = MyGroup('repr-group', driver_wrapper=desktop_driver)
    mobile_info = repr(mobile_group)
    desktop_info = repr(desktop_group)

    assert 'Group' in mobile_info
    assert 'locator="[id="repr-group"]"' in mobile_info
    assert 'locator_type="css selector"' in mobile_info
    assert 'name="repr-group"' in mobile_info
    assert 'parent=None' in mobile_info
    assert 'at 0x' in mobile_info
    assert '1_driver' in mobile_info
    assert 'appium.webdriver.webdriver.WebDriver' in mobile_info

    assert 'Group' in desktop_info
    assert 'locator="repr-group"' in desktop_info
    assert 'locator_type="id"' in desktop_info
    assert 'name="repr-group"' in desktop_info
    assert 'parent=None' in desktop_info
    assert 'at 0x' in desktop_info
    assert '2_driver' in desktop_info
    assert 'selenium.webdriver' in desktop_info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_mobile_and_desktop_page_repr(driver, request):
    mobile_driver = request.getfixturevalue(driver)
    desktop_driver = request.getfixturevalue('mocked_selenium_driver')
    mobile_page = Page('repr-page', driver_wrapper=mobile_driver)
    desktop_page = Page('repr-page', driver_wrapper=desktop_driver)
    mobile_info = repr(mobile_page)
    desktop_info = repr(desktop_page)

    assert 'Page' in mobile_info
    assert 'locator="[id="repr-page"]"' in mobile_info
    assert 'locator_type="css selector"' in mobile_info
    assert 'name="repr-page"' in mobile_info
    assert 'parent=None' in mobile_info
    assert 'at 0x' in mobile_info
    assert '1_driver' in mobile_info
    assert 'appium.webdriver.webdriver.WebDriver' in mobile_info

    assert 'Page' in desktop_info
    assert 'locator="repr-page"' in desktop_info
    assert 'locator_type="id"' in desktop_info
    assert 'name="repr-page"' in desktop_info
    assert 'parent=None' in desktop_info
    assert 'at 0x' in desktop_info
    assert '2_driver' in desktop_info
    assert 'selenium.webdriver' in desktop_info
