import time
from logging import info

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from dyatel.utils import cut_log_data
from dyatel.internal_utils import get_child_elements, Mixin
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.utils import get_locator_type, get_legacy_selector


ELEMENT_WAIT = 10


class CoreElement(Mixin):
    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver = CoreDriver.driver
        self.driver_wrapper = CoreDriver(self.driver)
        self.parent = parent if parent else None

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

        self.child_elements = get_child_elements(self, CoreElement)
        for el in self.child_elements:  # required for Group # TODO: maybe need to replace with function call
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get playwright element

        :param args: args from Locator object
        :param kwargs: kwargs from Locator object
        :return: Locator
        """
        return self._get_driver().find_element(self.locator_type, self.locator)

    @property
    def all_elements(self) -> list:
        """
        Get all playwright elements, matching given locator

        :return: list of elements
        """
        return self._get_driver().find_elements(self.locator_type, self.locator)

    # Element interaction

    def type_text(self, text, silent=False):
        """
        Type text to current element

        :param text: text to be typed
        :param silent: erase log
        :return: self
        """
        text = str(text)
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')

        self.wait_element(silent=True).element.send_keys(text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, silent=False):
        """
        Type text to current element slowly

        :param text: text to be slowly typed
        :param sleep_gap: sleep gap before each key press
        :param silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            info(f'Type text "{cut_log_data(text)}" into "{self.name}"')

        self.wait_element(silent=True)
        for letter in str(text):
            self.element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, silent=False):
        """
        Clear text from current element

        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Clear text in "{self.name}"')

        self.wait_element(silent=True).element.clear()
        return self

    # Element waits

    def wait_element(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait for current element available in page

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}"')

        message = f'Can\'t wait element "{self.name}". {self._get_element_logging_data()}'
        self._get_wait(timeout).until(
            EC.visibility_of_element_located((self.locator_type, self.locator)), message=message
        )
        return self

    def wait_element_hidden(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait for current element available in page without raising error

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait hidden of "{self.name}"')

        is_hidden = False
        start_time = time.time()

        while time.time() - start_time < timeout and not is_hidden:
            try:
                is_hidden = not self.element.is_displayed()
            except (NoSuchElementException, StaleElementReferenceException):
                is_hidden = True

        if not is_hidden:
            raise Exception(f'Element "{self.name}" still visible. {self._get_element_logging_data()}')

        return self

    def wait_element_without_error(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait until element hidden

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except (NoSuchElementException, TimeoutException, WebDriverException) as exception:
            info(f'Ignored exception: "{exception}"')
        return self

    def wait_clickable(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Compatibility placeholder
        Wait until element clickable

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until clickable of "{self.name}"')

        message = f'Element "{self.name}" not clickable. {self._get_element_logging_data()}'
        self._get_wait(timeout).until(
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
    def get_inner_text(self):
        text = self.get_attribute('textContent') or self.get_attribute('innerText')
        return text

    @property
    def get_value(self):
        return self.get_attribute('value')

    def is_displayed(self):
        result = False
        if self.is_available():
            result = self.element.is_displayed()
        info(f'Check displaying of "{self.name}"')
        return result

    def get_attribute(self, attribute, silent=False):
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')
        return self.wait_element(silent=True).element.get_attribute(attribute)

    def get_elements_texts(self, silent=False):
        if not silent:
            info(f'Get all texts from "{self.name}"')

        self.wait_element(silent=True)
        return (element_item.text for element_item in self.all_elements)

    def get_elements_count(self, silent=False):
        if not silent:
            info(f'Get elements count of "{self.name}"')

        self.wait_element(silent=True)
        return len(self.all_elements)

    # Mixin

    def _get_driver(self):
        """
        Get driver including parent element if available
        """
        base = self.driver
        if self.parent:
            base = self.parent.element
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base

    def _get_wait(self, timeout=ELEMENT_WAIT):
        return WebDriverWait(self._get_driver(), timeout)
