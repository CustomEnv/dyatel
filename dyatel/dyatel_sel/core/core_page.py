from logging import info

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.utils import get_locator_type, get_legacy_selector


def _get_page_elements(self):
    """Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    page_elements = []

    class_items = list(self.__dict__.items()) + list(self.__class__.__dict__.items())

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    for attribute, value in list(self.__class__.__dict__.items()):
        if isinstance(value, CoreElement):
            page_elements.append(value)
    return page_elements


class CorePage:
    def __init__(self, locator, locator_type=None, name=None):
        self.driver = CoreDriver.driver
        self.driver_wrapper = CoreDriver(self.driver)
        self.url = getattr(self, 'url', '')

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

        self.page_elements: list = _get_page_elements(self)
        for el in self.page_elements:  # required for CoreElement
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

        self.wait = WebDriverWait(self.driver, 10)

    def refresh(self, wait_page_load=True):
        info(f'Reload {self.name} page')
        self.driver.refresh()
        if wait_page_load:
            self.wait_page_loaded()
        return self

    def open_page(self, url=''):
        url = self.url if not url else url
        self.driver_wrapper.get(url)
        self.wait_page_loaded()
        return self

    def wait_page_loaded(self, silent=False):
        if not silent:
            info(f'Wait presence of "{self.name}"')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self

    def page_opened(self):
        if self.url:
            return self.driver.current_url == self.url
        else:
            return self.driver.find_element(by=self.locator_type, value=self.locator).is_displayed()
