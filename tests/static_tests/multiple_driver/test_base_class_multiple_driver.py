from dyatel.base.group import Group
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.base.page import Page
from dyatel.base.element import Element
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


class TestPage1(Page):
    el1 = Element('el1')


class TestPage2(Page):
    el2 = Element('el2')


class Group1(Group):
    gel1 = Element('gel1')


class Group2(Group):
    gel2 = Element('gel2')


# Appium + Selenium


def test_base_page_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_page = TestPage1('locator', driver_wrapper=mocked_ios_driver)
    desktop_page = TestPage2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_page.__class__.__base__ == MobilePage
    assert desktop_page.__class__.__base__ == WebPage


def test_base_page_element_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_page = TestPage1('locator', driver_wrapper=mocked_ios_driver)
    desktop_page = TestPage2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_page.el1.__class__.__base__ == MobileElement
    assert desktop_page.el2.__class__.__base__ == WebElement


def test_base_group_class_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_group = Group1('locator', driver_wrapper=mocked_ios_driver)
    desktop_group = Group2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_group.__class__.__base__ == MobileElement
    assert desktop_group.__class__.__base__ == WebElement


def test_base_group_element_class_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_group = Group1('locator', driver_wrapper=mocked_ios_driver)
    desktop_group = Group2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_group.gel1.__class__.__base__ == MobileElement
    assert desktop_group.gel2.__class__.__base__ == WebElement
