import pytest
from mock.mock import MagicMock

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.base.page import Page
from dyatel.base.element import Element
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


@pytest.fixture
def mocked_mobile_driver():
    driver = MagicMock()
    driver.capabilities = MagicMock(return_value={'platformName': 'ios', 'browserName': 'safari'})()
    return MobileDriver(driver)


@pytest.fixture
def mocked_web_driver():
    return WebDriver(MagicMock())


def test_base_page_mobile(mocked_mobile_driver):
    base_page = Page('locator')
    assert all((base_page.root_page_class == MobilePage, CoreDriver.mobile))


def test_base_element_mobile(mocked_mobile_driver):
    base_element = Element('locator')
    assert all((base_element.root_element_class == MobileElement, CoreDriver.mobile))


def test_base_page_web(mocked_web_driver):
    base_page = Page('locator')
    assert all((base_page.root_page_class == WebPage, not CoreDriver.mobile))


def test_base_element_web(mocked_web_driver):
    base_element = Element('locator')
    assert all((base_element.root_element_class == WebElement, not CoreDriver.mobile))
