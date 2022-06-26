import time
from logging import info

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from dyatel.shared_utils import cut_log_data
from dyatel.internal_utils import get_child_elements, Mixin
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.sel_utils import get_locator_type, get_legacy_selector


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

        self._element = None

        self.child_elements = get_child_elements(self, CoreElement)
        for el in self.child_elements:  # required for Group # TODO: maybe need to replace with function call
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium element

        :return: Locator
        """
        try:
            driver = self._get_driver()
        except NoSuchElementException:
            message = f'Cant find parent element "{self.parent.name}". {self.get_element_logging_data(self.parent)}.'
            raise NoSuchElementException(message) from NoSuchElementException

        try:
            element = driver.find_element(self.locator_type, self.locator)
        except NoSuchElementException:
            message = f'Cant find element "{self.name}". {self.get_element_logging_data()}.'
            raise NoSuchElementException(message) from NoSuchElementException
        return self._element if self._element else element

    @element.setter
    def element(self, selenium_element):
        """
        Current class element setter. Try to avoid usage of this function

        :param: selenium_element: selenium WebElement object, that will be set for current class
        """
        self._element = selenium_element

    # Element interaction

    def click(self):
        """
        Click to current element

        :return: self
        """
        info(f'Click into "{self.name}"')
        self.wait_element(silent=True).wait_clickable(silent=True).element.click()
        return self

    def type_text(self, text, silent=False):
        """
        Type text to current element

        :param: text: text to be typed
        :param: silent: erase log
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

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
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

        :param: silent: erase log
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

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}"')

        message = f'Can\'t wait element "{self.name}". {self.get_element_logging_data()}'
        self._get_wait(timeout).until(
            ec.visibility_of_element_located((self.locator_type, self.locator)), message=message
        )
        return self

    def wait_element_without_error(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except (NoSuchElementException, TimeoutException, WebDriverException) as exception:
            info(f'Ignored exception: "{exception}"')
        return self

    def wait_element_hidden(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
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
            raise Exception(f'Element "{self.name}" still visible. {self.get_element_logging_data()}')

        return self

    def wait_clickable(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Compatibility placeholder
        Wait until element clickable

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until clickable of "{self.name}"')

        message = f'Element "{self.name}" not clickable. {self.get_element_logging_data()}'
        self._get_wait(timeout).until(
            ec.element_to_be_clickable((self.locator_type, self.locator)), message=message
        )
        return self

    # Element state

    def scroll_into_view(self, block='center', behavior='instant', sleep=0):
        """
        Scroll element into view by js script

        :param: block: start - element on the top; end - element at the bottom
        :param: behavior: scroll type: smooth or instant
        :return: self
        """
        info(f'Scroll element "{self.name}" into view')

        self.wait_element(silent=True)

        self.driver.execute_script(
            'arguments[0].scrollIntoView({{block: "{}", behavior: "{}"}});'.format(block, behavior), self.element
        )

        if sleep:
            time.sleep(sleep)

        return self

    def get_screenshot(self, filename):
        info(f'Get screenshot of "{self.name}"')
        image_binary = self.get_screenshot_base
        image_binary.save(filename)
        return image_binary

    @property
    def get_screenshot_base(self):
        screenshot_binary = self.element.screenshot_as_png
        el_width = self.element.size['width']
        return self.scaled_screenshot(screenshot_binary, el_width)

    @property
    def get_text(self):
        """
        Get current element text

        :return: element text
        """
        info(f'Get text from "{self.name}"')
        return self.element.text

    @property
    def get_inner_text(self):
        """
        Get current element inner text

        :return: element inner text
        """
        text = self.get_attribute('textContent') or self.get_attribute('innerText')
        return text

    @property
    def get_value(self):
        """
        Get value from current element

        :return: element value
        """
        return self.get_attribute('value')

    def is_available(self):
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        return bool(len(getattr(self, 'all_elements')))

    def is_displayed(self):
        """
        Check visibility of element

        :return: True if element visible
        """
        result = False
        if self.is_available():  # Check in DOM first due to selenium exception
            result = self.element.is_displayed()
        info(f'Check displaying of "{self.name}"')
        return result

    def is_hidden(self):
        """
        Check invisibility of current element

        :return: True if element hidden
        """
        return not self.is_displayed()

    def get_attribute(self, attribute, silent=False):
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')

        return self.wait_element(silent=True).element.get_attribute(attribute)

    def get_elements_texts(self, silent=False) -> list:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            info(f'Get all texts from "{self.name}"')

        self.wait_element(silent=True)
        return list(element_item.text for element_item in getattr(self, 'all_elements'))

    def get_elements_count(self, silent=False):
        """
        Get elements count

        :param: silent: erase log
        :return: elements count
        """
        if not silent:
            info(f'Get elements count of "{self.name}"')

        self.wait_element(silent=True)
        return len(getattr(self, 'all_elements'))

    # Mixin

    def _get_driver(self):
        """
        Get driver with depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            base = self.parent.element
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base

    def _get_wait(self, timeout=ELEMENT_WAIT) -> WebDriverWait:
        """
        Get wait with depends on parent element if available

        :return: driver
        """
        return WebDriverWait(self._get_driver(), timeout)

    @property
    def _action_chains(self) -> ActionChains:
        """
        Get action chains with depends on parent element if available

        :return: ActionChains
        """
        return ActionChains(self._get_driver())
