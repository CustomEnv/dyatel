import time
from logging import info

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from data_for_testing.utils import cut_log_data
from selenium_master.core.core_driver import CoreDriver
from selenium_master.utils import get_locator_type, get_legacy_selector


ELEMENT_WAIT = 10


class CoreElement:
    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        self.driver_wrapper = CoreDriver(self.driver)
        self.parent = parent if parent else None
        self.parent_selenium = getattr(self.parent, 'element') if self.parent else None
        self._elements = None

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

    # Element

    @property
    def element(self):
        if not self._elements:
            self._elements = self.get_driver().find_element(self.locator_type, self.locator)

        is_multiple_elements = type(self._elements) in (list, tuple, dict, set, frozenset)
        return self._elements[0] if is_multiple_elements else self._elements

    @property
    def all_elements(self):
        if not self._elements:
            self._elements = self.get_driver().find_elements(self.locator_type, self.locator)

        return self._elements

    # Element interaction

    def type_text(self, text, wait=True, silent=False):
        text = str(text)
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')
        self.element.send_keys(text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, wait=True, silent=False):
        text = str(text)
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Type text "{cut_log_data(text)}" into "{self.name}"')
        for letter in str(text):
            self.element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Clear text in "{self.name}"')
        self.element.clear()
        return self

    # Element waits

    def wait_element(self, silent=False, timeout=ELEMENT_WAIT):
        if not silent:
            info(f'Wait until presence of "{self.name}"')

        message = f'Can\'t wait element "{self.name}". Locator type: "{self.locator_type}". Locator: "{self.locator}"'
        self.get_wait(timeout).until(
            EC.visibility_of_element_located((self.locator_type, self.locator)), message=message
        )
        return self

    def wait_element_hidden(self, silent=False, timeout=ELEMENT_WAIT):
        if not silent:
            info(f'Wait hidden of "{self.name}"')

        message = f'Element "{self.name}" still visible. Locator type: "{self.locator_type}". Locator: "{self.locator}"'
        self.get_wait(timeout).until_not(
            EC.visibility_of_element_located((self.locator_type, self.locator)), message=message
        )
        return self

    def wait_element_without_error(self, silent=False, timeout=ELEMENT_WAIT):
        if not silent:
            info(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(silent=True, timeout=timeout)
        except (NoSuchElementException, TimeoutException, WebDriverException) as exception:
            info(f'Ignored exception: "{exception}"')
        return self

    def wait_clickable(self, silent=False, timeout=ELEMENT_WAIT):
        if not silent:
            info(f'Wait until clickable of "{self.name}"')

        message = f'Element "{self.name}" not clickable. Locator type: "{self.locator_type}". Locator: "{self.locator}"'
        self.get_wait(timeout).until(
            EC.element_to_be_clickable((self.locator_type, self.locator)), message=message
        )
        return self

    # Element state

    def is_available(self):
        return bool(len(self.all_elements))

    @property
    def get_text(self):
        info(f'Get text from {self.name}')
        return self.element.text

    @property
    def get_raw_text(self):
        return self.get_attribute('textContent')

    @property
    def get_inner_text(self):
        return self.get_attribute('innerText')

    @property
    def get_value(self):
        return self.get_attribute('value')

    def is_displayed(self):
        result = False
        if self.is_available():
            result = self.element.is_displayed()
        info(f'Check displaying of "{self.name}"')
        return result

    def get_attribute(self, attribute, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')
        return self.element.get_attribute(attribute)

    def get_elements_texts(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Get all texts from "{self.name}"')
        return (element_item.text for element_item in self.all_elements)

    def get_elements_count(self, wait=True, silent=False):
        if wait:
            self.wait_element(silent=True)
        if not silent:
            info(f'Get elements count of "{self.name}"')
        return len(self.all_elements)

    # Mixin

    def get_driver(self):
        """
        Get driver including parent element if available
        """
        base = self.parent_selenium if self.parent_selenium else self.driver
        if self.parent:
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base

    def get_wait(self, timeout=ELEMENT_WAIT):
        return WebDriverWait(self.driver, timeout)
