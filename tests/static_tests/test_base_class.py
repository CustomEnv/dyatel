from dyatel.base.group import Group
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.base.page import Page
from dyatel.base.element import Element
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


# Appium


def test_base_page_mobile(mocked_mobile_driver):
    page = Page('locator')
    assert page.__class__.__base__ == MobilePage


def test_base_element_mobile(mocked_mobile_driver):
    element = Element('locator')
    assert element.__class__.__base__ == MobileElement


def test_base_group_class_mobile(mocked_mobile_driver):
    group = Group('locator')
    assert group.__class__.__base__ == Element


# Selenium


def test_base_page_selenium(mocked_selenium_driver):
    page = Page('locator')
    assert page.__class__.__base__ == WebPage


def test_base_element_selenium(mocked_selenium_driver):
    element = Element('locator')
    assert element.__class__.__base__ == WebElement


def test_base_group_class_selenium(mocked_selenium_driver):
    group = Group('locator')
    assert group.__class__.__base__ == Element


# Playwright


def test_base_page_playwright(mocked_play_driver):
    page = Page('locator')
    assert page.__class__.__base__ == PlayPage


def test_base_element_playwright(mocked_play_driver):
    element = Element('locator')
    assert element.__class__.__base__ == PlayElement


def test_base_group_class_playwright(mocked_play_driver):
    group = Group('locator')
    assert group.__class__.__base__ == Element
