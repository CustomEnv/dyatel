from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class Section(Group):
    def __init__(self):
        super().__init__('Section')

    el = Element('el')


class PageObject(Page):
    def __init__(self, driver_wrapper=None):
        self.section = Section()
        super().__init__('PageObject', driver_wrapper=driver_wrapper)


def test_driver_in_page(mocked_android_driver, mocked_selenium_driver):
    mobile_page = PageObject(driver_wrapper=mocked_android_driver)
    desktop_page = PageObject(driver_wrapper=mocked_selenium_driver)

    assert mobile_page.driver_wrapper == mocked_android_driver
    assert desktop_page.driver_wrapper == mocked_selenium_driver

    assert mobile_page.section.driver_wrapper == mocked_android_driver
    assert desktop_page.section.driver_wrapper == mocked_selenium_driver

    assert mobile_page.section.el.driver_wrapper == mocked_android_driver
    assert desktop_page.section.el.driver_wrapper == mocked_selenium_driver
