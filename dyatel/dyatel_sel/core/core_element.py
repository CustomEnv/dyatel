import time
from logging import info

from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from dyatel.utils import cut_log_data
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.utils import get_locator_type, get_legacy_selector


ELEMENT_WAIT = 10


def get_dict_attr(obj, attr):
    for obj in [obj] + obj.__class__.mro():
        if attr in obj.__dict__:
            return obj.__dict__[attr]  # issue here


def _get_child_elements(self):
    """Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements = []

    class_items = list(self.__dict__.items()) + list(self.__class__.__dict__.items())

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    for attr_name in self.__dir__():
        attr_value = get_dict_attr(self, attr_name)
        if self.name == 'Parent Group':
            breakpoint()
        if attr_name == 'parent_element_init_var':
            breakpoint()
        class_items.append((attr_name, attr_value))

    for attribute, value in class_items:
        if attribute == 'parent_element_init_var':
            breakpoint()
        if isinstance(value, CoreElement):
            elements.append(value)
    return set(elements)


class CoreElement:
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

        self.child_elements = _get_child_elements(self)

        for el in self.child_elements:  # required for Group
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    # Element

    @property
    def element(self):
        return self._get_driver().find_element(self.locator_type, self.locator)

    @property
    def all_elements(self):
        return self._get_driver().find_elements(self.locator_type, self.locator)

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

        message = f'Can\'t wait element "{self.name}". {self._get_element_logging_data(self)}'
        self._get_wait(timeout).until(
            EC.visibility_of_element_located((self.locator_type, self.locator)), message=message
        )
        return self

    def wait_element_hidden(self, silent=False, timeout=ELEMENT_WAIT):
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
            raise Exception(f'Element "{self.name}" still visible. {self._get_element_logging_data(self)}')

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

        message = f'Element "{self.name}" not clickable. {self._get_element_logging_data(self)}'
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

    def _get_element_logging_data(self, element):
        current = element
        parent = current.parent
        current_data = f'Selector: ["{self.locator_type}": "{self.locator}"]'
        if parent:
            parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
            current_data = f'{current_data}. {parent_data}'
        return current_data

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
