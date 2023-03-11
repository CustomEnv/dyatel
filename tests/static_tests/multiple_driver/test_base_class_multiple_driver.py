import pytest

from dyatel.base.group import Group
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.base.page import Page
from dyatel.base.element import Element
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


class Page1(Page):
    el1 = Element('el1')


class Page2(Page):
    el2 = Element('el2')


class Group1(Group):
    gel1 = Element('gel1')


class Group2(Group):
    gel2 = Element('gel2')


class ParentPage(Page):
    el1 = Element('el1')


class ChildPage(ParentPage):
    el2 = Element('el2')


class ChildPage2(ChildPage):
    el3 = Element('el3')


class PageWithInit(Page):
    def __init__(self, locator='page.with.init', driver_wrapper=None):
        self.el1 = Element('1')
        super().__init__(locator=locator, name='page with init', driver_wrapper=driver_wrapper)


class ChildPageWithInit(PageWithInit):
    def __init__(self, locator='child.page.with.init', driver_wrapper=None):
        self.el2 = Element('2')
        super().__init__(locator=locator, driver_wrapper=driver_wrapper)


class ChildPageWithoutInit(ChildPageWithInit):
    el3 = Element('3')


# Appium + Selenium


@pytest.mark.skip('rework needed')
def test_base_page_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_page = Page1('locator', driver_wrapper=mocked_ios_driver)
    desktop_page = Page2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_page.__class__.__base__ == MobilePage
    assert desktop_page.__class__.__base__ == WebPage


@pytest.mark.skip('rework needed')
def test_base_group_class_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_group = Group1('locator', driver_wrapper=mocked_ios_driver)
    desktop_group = Group2('locator', driver_wrapper=mocked_selenium_driver)
    assert mobile_group.__class__.__base__ == MobileElement
    assert desktop_group.__class__.__base__ == WebElement


@pytest.mark.skip('rework needed')
def test_base_group_element_class_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_group = Group1('group1', driver_wrapper=mocked_ios_driver)
    desktop_group = Group2('group2', driver_wrapper=mocked_selenium_driver)

    assert 'Shadow' in str(mobile_group.gel1.__class__)
    assert 'Shadow' in str(desktop_group.gel2.__class__)

    assert mobile_group.gel1.__class__.__base__ == MobileElement
    assert desktop_group.gel2.__class__.__base__ == WebElement


@pytest.mark.skip('rework needed')
def test_base_page_mobile_and_desktop_with_tree_and_init(mocked_ios_driver, mocked_selenium_driver):
    mobile_page_with_init = ChildPageWithInit(driver_wrapper=mocked_ios_driver)
    mobile_page_without_init = ChildPageWithoutInit(driver_wrapper=mocked_ios_driver)
    desktop_page_with_init = ChildPageWithInit(driver_wrapper=mocked_selenium_driver)
    desktop_page_without_init = ChildPageWithoutInit(driver_wrapper=mocked_selenium_driver)

    assert mobile_page_without_init.__class__.__bases__[0] == MobilePage
    assert mobile_page_without_init.el3
    assert mobile_page_without_init.el2
    assert mobile_page_without_init.el1

    assert desktop_page_without_init.__class__.__bases__[0] == WebPage
    assert desktop_page_without_init.el3
    assert desktop_page_without_init.el2
    assert desktop_page_without_init.el1

    assert mobile_page_with_init.__class__.__bases__[0] == MobilePage
    assert mobile_page_with_init.el2
    assert mobile_page_with_init.el1

    assert desktop_page_with_init.__class__.__bases__[0] == WebPage
    assert desktop_page_with_init.el2
    assert desktop_page_with_init.el1

    assert 'child.page.with.init' in desktop_page_with_init.locator
    assert 'child.page.with.init' in mobile_page_with_init.locator


@pytest.mark.skip('rework needed')
def test_base_page_element_mobile_and_desktop(mocked_ios_driver, mocked_selenium_driver):
    mobile_page = Page1('locator', driver_wrapper=mocked_ios_driver)
    desktop_page = Page2('locator', driver_wrapper=mocked_selenium_driver)

    assert 'Shadow' in str(mobile_page.el1.__class__)
    assert 'Shadow' in str(desktop_page.el2.__class__)

    assert mobile_page.el1.__class__.__base__ == MobileElement
    assert desktop_page.el2.__class__.__base__ == WebElement


@pytest.mark.skip('rework needed')
def test_base_page_mobile_and_desktop_with_tree(mocked_ios_driver, mocked_selenium_driver):
    mobile_page = ChildPage2('locator', driver_wrapper=mocked_ios_driver)
    desktop_page = ChildPage2('locator', driver_wrapper=mocked_selenium_driver)

    assert mobile_page.__class__.__base__ == MobilePage

    assert mobile_page.el1
    assert mobile_page.el1.__class__.__base__ == MobileElement

    assert mobile_page.el2
    assert mobile_page.el2.__class__.__base__ == MobileElement

    assert mobile_page.el3
    assert mobile_page.el3.__class__.__base__ == MobileElement

    assert desktop_page.__class__.__base__ == WebPage

    assert desktop_page.el1
    assert desktop_page.el1.__class__.__base__ == WebElement

    assert desktop_page.el2
    assert desktop_page.el2.__class__.__base__ == WebElement

    assert desktop_page.el3
    assert desktop_page.el3.__class__.__base__ == WebElement
