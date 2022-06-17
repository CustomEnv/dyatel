import pytest
from mock.mock import MagicMock

from selenium_master.core.core_driver import CoreDriver
from selenium_master.driver.mobile_driver import MobileDriver
from selenium_master.driver.web_driver import WebDriver
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement
from selenium_master.base.base_page import BasePage
from selenium_master.base.base_element import BaseElement
from selenium_master.pages.mobile_page import MobilePage
from selenium_master.pages.web_page import WebPage


@pytest.fixture
def mocked_mobile_driver():
    driver = MagicMock()
    driver.capabilities = MagicMock(return_value={'platformName': 'ios', 'browserName': 'safari'})()
    return MobileDriver(driver)


@pytest.fixture
def mocked_web_driver():
    return WebDriver(MagicMock())


def test_base_page_mobile(mocked_mobile_driver):
    base_page = BasePage('locator')
    assert all((base_page.root_page_class == MobilePage, CoreDriver.mobile))


def test_base_element_mobile(mocked_mobile_driver):
    base_element = BaseElement('locator')
    assert all((base_element.root_element_class == MobileElement, CoreDriver.mobile))


def test_base_page_web(mocked_web_driver):
    base_page = BasePage('locator')
    assert all((base_page.root_page_class == WebPage, not CoreDriver.mobile))


def test_base_element_web(mocked_web_driver):
    base_element = BaseElement('locator')
    assert all((base_element.root_element_class == WebElement, not CoreDriver.mobile))
