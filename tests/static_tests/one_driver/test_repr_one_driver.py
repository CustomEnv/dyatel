import pytest

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page
from tests.static_tests.conftest import mobile_drivers, mobile_ids


def test_ios_driver_repr(mocked_ios_driver):
    info = repr(mocked_ios_driver)
    assert 'platform=ios' in info
    assert '1_driver' in info
    assert 'DriverWrapper' in info
    assert 'at 0x' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info


def test_android_driver_repr(mocked_android_driver):
    info = repr(mocked_android_driver)
    assert 'platform=android' in info
    assert '1_driver' in info
    assert 'DriverWrapper' in info
    assert 'at 0x' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info


def test_selenium_driver_repr(mocked_selenium_driver):
    info = repr(mocked_selenium_driver)
    assert 'platform=desktop' in info
    assert '1_driver' in info
    assert 'DriverWrapper' in info
    assert 'at 0x' in info
    assert 'selenium.webdriver' in info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_mobile_element_repr(driver, request):
    request.getfixturevalue(driver)
    info = repr(Element('element-repr'))
    assert 'Element' in info
    assert 'locator="[id="element-repr"]"' in info
    assert 'locator_type="css selector"' in info
    assert 'name="element-repr"' in info
    assert 'parent=NoneType' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info


def test_selenium_element_repr(mocked_selenium_driver):
    info = repr(Element('element-repr'))
    assert 'Element' in info
    assert 'locator="element-repr"' in info
    assert 'locator_type="id"' in info
    assert 'name="element-repr"' in info
    assert 'parent=NoneType' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'selenium.webdriver' in info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_mobile_group_repr(driver, request):
    request.getfixturevalue(driver)
    info = repr(Group('element-repr'))
    assert 'Group' in info
    assert 'locator="[id="element-repr"]"' in info
    assert 'locator_type="css selector"' in info
    assert 'name="element-repr"' in info
    assert 'parent=NoneType' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info


def test_selenium_group_repr(mocked_selenium_driver):
    info = repr(Group('element-repr'))
    assert 'Group' in info
    assert 'locator="element-repr"' in info
    assert 'locator_type="id"' in info
    assert 'name="element-repr"' in info
    assert 'parent=NoneType' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'selenium.webdriver' in info


def test_ios_page_repr(mocked_ios_driver):
    info = repr(Page('element-repr'))
    assert 'Page' in info
    assert 'locator="[id="element-repr"]"' in info
    assert 'locator_type="css selector"' in info
    assert 'name="element-repr"' in info
    assert 'parent=None' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_android_page_repr(driver, request):
    request.getfixturevalue(driver)
    info = repr(Page('element-repr'))
    assert 'Page' in info
    assert 'locator="[id="element-repr"]"' in info
    assert 'locator_type="css selector"' in info
    assert 'name="element-repr"' in info
    assert 'parent=None' in info
    assert 'at 0x' in info
    assert '1_driver' in info
    assert 'appium.webdriver.webdriver.WebDriver' in info
