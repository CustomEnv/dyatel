from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class Section(Group):
    def __init__(self, where: str):
        super().__init__(f'Section{where.title()}')

    el = Element('el')


class PageObject(Page):
    def __init__(self, where: str, driver_wrapper):
        self.section = Section(where)
        super().__init__('PageObject', driver_wrapper=driver_wrapper)


def test_driver_in_page(mocked_android_driver, mocked_selenium_driver):
    mobile_page = PageObject('mobile', driver_wrapper=mocked_android_driver)
    desktop_page = PageObject('desktop', driver_wrapper=mocked_selenium_driver)

    assert mobile_page.driver_wrapper == mocked_android_driver
    assert desktop_page.driver_wrapper == mocked_selenium_driver

    assert mobile_page.section.driver_wrapper == mocked_android_driver
    assert desktop_page.section.driver_wrapper == mocked_selenium_driver

    assert mobile_page.section.el.driver_wrapper == mocked_android_driver
    assert desktop_page.section.el.driver_wrapper == mocked_selenium_driver

    assert mobile_page.section.el.parent.driver_wrapper == mocked_android_driver
    assert desktop_page.section.el.parent.driver_wrapper == mocked_selenium_driver
