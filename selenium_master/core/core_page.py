from logging import info

from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_master.core.core_driver import CoreDriver
from selenium_master.utils import get_locator_type, get_legacy_selector


class CorePage:
    def __init__(self, locator, locator_type=None, name=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        self.driver_wrapper = CoreDriver(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = getattr(self, 'url', '')

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

    def refresh(self, wait_page_load=True):
        info(f'Reload {self.name} page')
        self.driver.refresh()
        if wait_page_load:
            self.wait_page_loaded()
        return self

    def open_page(self, url=''):
        url = self.url if not url else url
        info(f'Navigating to url {url}')
        self.driver.get(url)
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
