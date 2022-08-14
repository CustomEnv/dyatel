from __future__ import annotations

import time
from io import BytesIO
from typing import Union, List, Any

from PIL import Image
from selenium.common.exceptions import *
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from dyatel.mixins.log_mixin import LogMixin
from dyatel.shared_utils import cut_log_data
from dyatel.mixins.internal_utils import get_child_elements, WAIT_EL, initialize_objects_with_args
from dyatel.mixins.element_mixin import ElementMixin
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.dyatel_sel.core.core_driver import CoreDriver


class CoreElement(ElementMixin, DriverMixin, LogMixin):

    def __init__(self, locator: str, locator_type: str = '', name: str = '', parent: Any = None, wait: bool = False):
        """
        Initializing of core element with appium/selenium driver
        Contain same methods/data for both WebElement and MobileElement classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects
        """
        self._element = None
        self._initialized = True
        self._driver_instance = CoreDriver

        self.locator = locator
        self.locator_type = locator_type
        self.name = name if name else self.locator
        self.parent: Any = parent
        self.wait = wait

        self.child_elements: List[CoreElement] = get_child_elements(self, CoreElement)
        initialize_objects_with_args(self.child_elements)  # required for Group

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium WebElement object

        :return: Locator
        """
        return self._get_element(wait=True)

    @element.setter
    def element(self, selenium_element: SeleniumWebElement):
        """
        Current class element setter. Try to avoid usage of this function

        :param: selenium_element: selenium WebElement object, that will be set for current class
        """
        self._element = selenium_element

    # Element interaction

    def click(self) -> CoreElement:
        """
        Click to current element

        :return: self
        """
        self.log(f'Click into "{self.name}"')
        self.wait_element(silent=True).wait_clickable(silent=True).element.click()
        return self

    def type_text(self, text: str, silent: bool = False) -> CoreElement:
        """
        Type text to current element

        :param: text: text to be typed
        :param: silent: erase log
        :return: self
        """
        text = str(text)
        if not silent:
            self.log(f'Type text {cut_log_data(text)} into "{self.name}"')

        self.wait_element(silent=True).element.send_keys(text)
        return self

    def type_slowly(self, text: str, sleep_gap: float = 0.05, silent: bool = False) -> CoreElement:
        """
        Type text to current element slowly

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            self.log(f'Type text "{cut_log_data(text)}" into "{self.name}"')

        self.wait_element(silent=True)
        for letter in str(text):
            self.element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, silent: bool = False) -> CoreElement:
        """
        Clear text from current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Clear text in "{self.name}"')

        self.wait_element(silent=True).element.clear()
        return self

    # Element waits

    def wait_element(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in page

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}"')

        def safe_is_displayed():
            try:
                return self._get_element(wait=False).is_displayed()
            except (NoSuchElementException, TimeoutException, WebDriverException, Exception):
                return False

        start_time = time.time()
        while time.time() - start_time < timeout and not safe_is_displayed():
            pass

        if not safe_is_displayed():
            raise TimeoutException(f'Can\'t wait element "{self.name}". {self.get_element_logging_data()}') from None

        return self

    def wait_element_without_error(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except (NoSuchElementException, TimeoutException, WebDriverException, Exception) as exception:
            if not silent:
                self.log(f'Ignored exception: "{exception.msg}"')
        return self

    def wait_element_hidden(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait hidden of "{self.name}"')

        is_hidden = False
        start_time = time.time()

        while time.time() - start_time < timeout and not is_hidden:
            try:
                is_hidden = not self._get_element(wait=False).is_displayed()
            except (NoSuchElementException, StaleElementReferenceException):
                is_hidden = True

        if not is_hidden:
            raise Exception(f'Element "{self.name}" still visible. {self.get_element_logging_data()}') from None

        return self

    def wait_clickable(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element clickable

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" become clickable')

        start_time = time.time()
        while time.time() - start_time < timeout and not self.element.is_enabled():
            pass

        if not self.element.is_enabled():
            raise Exception(f'"{self.name}" not clickable') from None

        return self

    def wait_availability(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" will be available in DOM')

        start_time = time.time()

        while time.time() - start_time < timeout and not self.is_available():
            pass

        if not self.is_available():
            raise Exception(f'Can\'t wait element in DOM "{self.name}". {self.get_element_logging_data()}') from None

        return self

    # Element state

    def scroll_into_view(self, block: str = 'center', behavior: str = 'instant',
                         sleep: Union[int, float] = 0) -> CoreElement:
        """
        Scroll element into view by js script

        :param: block: start - element on the top; end - element at the bottom
        :param: behavior: scroll type: smooth or instant
        :param: sleep: delay after scroll
        :return: self
        """
        self.log(f'Scroll element "{self.name}" into view')

        self.wait_element(silent=True)

        self.driver.execute_script(
            'arguments[0].scrollIntoView({{block: "{}", behavior: "{}"}});'.format(block, behavior), self.element
        )

        if sleep:
            time.sleep(sleep)

        return self

    def get_screenshot(self, filename: str) -> Image:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :return: image binary
        """
        self.log(f'Get screenshot of "{self.name}"')
        image_binary = self.get_screenshot_base
        image_binary.save(filename)
        return image_binary

    @property
    def get_screenshot_base(self) -> Image:
        """
        Get driver width scaled screenshot binary of element without saving

        :return: screenshot binary
        """
        screenshot_binary = self.element.screenshot_as_png
        el_width = self.element.size['width']
        return self._scaled_screenshot(screenshot_binary, el_width)

    @property
    def get_text(self) -> str:
        """
        Get current element text

        :return: element text
        """
        return self.element.text

    @property
    def get_inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        return self.get_attribute('textContent', silent=True) or self.get_attribute('innerText', silent=True)

    @property
    def get_value(self) -> str:
        """
        Get value from current element

        :return: element value
        """
        return self.get_attribute('value', silent=True)

    def is_available(self) -> bool:
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        try:
            is_available = self._get_driver(wait=False).find_elements(self.locator_type, self.locator)
        except (InvalidArgumentException, InvalidSelectorException) as exc:
            if 'invalid locator' in exc.msg or 'is not a valid' in exc.msg:
                msg = f'"{self.name}" have invalid selector: ["{self.locator_type}": "{self.locator}"]'
                raise InvalidArgumentException(msg=msg) from None
            else:
                raise exc

        return bool(len(is_available))

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of element

        :param: silent: erase log
        :return: True if element visible
        """
        result = False

        if not silent:
            self.log(f'Check displaying of "{self.name}"')

        if self.is_available():  # Check in DOM first due to selenium exception
            result = self._get_element(wait=False).is_displayed()

        return result

    def is_hidden(self, silent: bool = False) -> bool:
        """
        Check invisibility of current element

        :param: silent: erase log
        :return: True if element hidden
        """
        if not silent:
            self.log(f'Check invisibility of "{self.name}"')

        return not self.is_displayed()

    def get_attribute(self, attribute: str, silent: bool = False) -> str:
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            self.log(f'Get "{attribute}" from "{self.name}"')

        return self.wait_element(silent=True).element.get_attribute(attribute)

    def get_elements_texts(self, silent: bool = False) -> List[str]:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            self.log(f'Get all texts from "{self.name}"')

        self.wait_element(silent=True)
        return list(element_item.get_text for element_item in getattr(self, 'all_elements'))

    def get_elements_count(self, silent: bool = False) -> int:
        """
        Get elements count

        :param: silent: erase log
        :return: elements count
        """
        if not silent:
            self.log(f'Get elements count of "{self.name}"')

        return len(getattr(self, 'all_elements'))

    # Mixin

    def _get_driver(self, wait: bool = True) -> Union[SeleniumWebDriver, SeleniumWebElement]:
        """
        Get driver with depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            self.log(f'Get element "{self.name}" from parent element "{self.parent.name}"', level='debug')

            if isinstance(self.parent, CoreElement):
                base = self.parent._get_element(wait=wait)
            else:
                get_element_func = getattr(self.parent.anchor, '_get_element')
                base = get_element_func(wait=wait)

            if not base:
                raise NoSuchElementException('Can\'t specify parent element') from None

        if not base:
            raise Exception('Can\'t specify driver') from None

        return base

    def _get_wait(self, timeout: int = WAIT_EL) -> WebDriverWait:
        """
        Get wait with depends on parent element if available

        :return: driver
        """
        return WebDriverWait(self.driver, timeout)

    @property
    def _action_chains(self) -> ActionChains:
        """
        Get action chains with depends on parent element if available

        :return: ActionChains
        """
        return ActionChains(self.driver)

    def _scaled_screenshot(self, screenshot_binary: bin, width: int) -> Image:
        """
        Get scaled screenshot to fit driver window / element size

        :param screenshot_binary: original screenshot binary
        :param width: driver or element width
        :return: scaled image binary
        """
        img_binary = Image.open(BytesIO(screenshot_binary))
        scale = img_binary.size[0] / width

        if scale != 1:
            new_image_size = (int(img_binary.size[0] / scale), int(img_binary.size[1] / scale))
            img_binary = img_binary.resize(new_image_size, Image.ANTIALIAS)

        return img_binary

    def _get_element(self, wait: bool = True) -> SeleniumWebElement:
        """
        Get selenium element from driver or parent element

        :param wait: wait for element or element parent before grab
        :return: Locator
        """
        element = self._element

        if not element:
            try:
                driver = self._get_driver(wait=wait)
            except NoSuchElementException:
                parent = self.parent
                message = f'Cant find parent element "{parent.name}". {self.get_element_logging_data(parent)}.'
                raise NoSuchElementException(message) from None

            try:
                if wait:
                    self.wait_element(silent=True)
                element = driver.find_element(self.locator_type, self.locator)
            except NoSuchElementException:
                message = f'Cant find element "{self.name}". {self.get_element_logging_data()}.'
                raise NoSuchElementException(message) from None

        if not element:
            raise NoSuchElementException('Can\'t find element') from None

        return element
