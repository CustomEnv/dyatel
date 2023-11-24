import random
import time

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page
from tests.adata.pages.expected_condition_page import ExpectedConditionPage


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


count = 50


def test_scall(mocked_selenium_driver):
    for _ in range(5):
        start = time.time()
        [ExpectedConditionPage() for _ in range(count)]
        print(time.time() - start)


def test_call(mocked_selenium_driver):
    for _ in range(5):
        start = time.time()
        [ExpectedConditionPage(mocked_selenium_driver) for _ in range(count)]
        print(time.time() - start)


def test_xcall(mocked_selenium_driver, mocked_android_driver):
    for _ in range(5):
        start = time.time()
        [ExpectedConditionPage(random.choice([mocked_selenium_driver, mocked_android_driver])) for _ in range(count)]
        print(time.time() - start)
