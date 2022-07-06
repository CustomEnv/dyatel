from __future__ import annotations

import time
from io import BytesIO
from logging import info, debug
from typing import Union, List, Any

from PIL import Image
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from dyatel.shared_utils import cut_log_data
from dyatel.internal_utils import get_child_elements, Mixin, WAIT_EL
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.sel_utils import get_locator_type, get_legacy_selector


class CoreElement(Mixin):

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False):
        """
        Initializing of core element with appium/selenium driver
        Contain same methods/data for both WebElement and MobileElement classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects
        """
        self.parent: Union[CoreElement, Any] = parent if parent else None
        self.wait = wait

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

        self._element = None
        self._initialized = True

        self.child_elements: List[CoreElement] = get_child_elements(self, CoreElement)
        for el in self.child_elements:  # required for Group  # TODO: maybe need to replace with function call
            if not getattr(el, '_initialized'):
                el.__init__(
                    locator=el.locator,
                    locator_type=el.locator_type,
                    name=el.name,
                    parent=el.parent,
                    wait=el.wait,
                )

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium element

        :return: Locator
        """
        return self._get_element(wait=True)

    @element.setter
    def element(self, selenium_element):
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
        info(f'Click into "{self.name}"')
        self.wait_element(silent=True).wait_clickable(silent=True).element.click()
        return self

    def type_text(self, text, silent=False) -> CoreElement:
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

    def type_slowly(self, text, sleep_gap=0.05, silent=False) -> CoreElement:
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

    def clear_text(self, silent=False) -> CoreElement:
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

    def wait_element(self, timeout=WAIT_EL, silent=False) -> CoreElement:
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

    def wait_element_without_error(self, timeout=WAIT_EL, silent=False) -> CoreElement:
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
            if not silent:
                info(f'Ignored exception: "{exception}"')
        return self

    def wait_element_hidden(self, timeout=WAIT_EL, silent=False) -> CoreElement:
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
                is_hidden = not self._get_element(wait=False).is_displayed()
            except (NoSuchElementException, StaleElementReferenceException):
                is_hidden = True

        if not is_hidden:
            raise Exception(f'Element "{self.name}" still visible. {self.get_element_logging_data()}')

        return self

    def wait_clickable(self, timeout=WAIT_EL, silent=False) -> CoreElement:
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

    def scroll_into_view(self, block='center', behavior='instant', sleep=0) -> CoreElement:
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

    def get_screenshot(self, filename) -> Image:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :return: image binary
        """
        info(f'Get screenshot of "{self.name}"')
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
        info(f'Get text from "{self.name}"')
        return self.element.text

    @property
    def get_inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        text = self.get_attribute('textContent') or self.get_attribute('innerText')
        return text

    @property
    def get_value(self) -> str:
        """
        Get value from current element

        :return: element value
        """
        return self.get_attribute('value')

    def is_available(self) -> bool:
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        is_available = self._get_driver(wait=False).find_elements(self.locator_type, self.locator)
        return bool(len(is_available))

    def is_displayed(self, silent=False) -> bool:
        """
        Check visibility of element

        :param: silent: erase log
        :return: True if element visible
        """
        result = False

        if not silent:
            info(f'Check displaying of "{self.name}"')

        if self.is_available():  # Check in DOM first due to selenium exception
            result = self._get_element(wait=False).is_displayed()

        return result

    def is_hidden(self, silent=False) -> bool:
        """
        Check invisibility of current element

        :param: silent: erase log
        :return: True if element hidden
        """
        if not silent:
            info(f'Check invisibility of "{self.name}"')

        return not self.is_displayed()

    def get_attribute(self, attribute, silent=False) -> str:
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')

        return self.wait_element(silent=True).element.get_attribute(attribute)

    def get_elements_texts(self, silent=False) -> List[str]:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            info(f'Get all texts from "{self.name}"')

        self.wait_element(silent=True)
        return list(element_item.text for element_item in getattr(self, 'all_elements'))

    def get_elements_count(self, silent=False) -> int:
        """
        Get elements count

        :param: silent: erase log
        :return: elements count
        """
        if not silent:
            info(f'Get elements count of "{self.name}"')

        self.wait_element(silent=True)
        return len(getattr(self, 'all_elements'))

    @property
    def driver(self) -> Union[AppiumWebDriver, SeleniumWebDriver]:
        """
        Get source driver instance

        :return: SeleniumWebDriver for web test or AppiumWebDriver for mobile tests
        """
        return CoreDriver.driver

    @property
    def driver_wrapper(self) -> CoreDriver:
        """
        Get source driver wrapper instance

        :return: CoreDriver
        """
        return CoreDriver.driver_wrapper

    # Mixin

    def _get_driver(self, wait=True) -> Union[SeleniumWebDriver, SeleniumWebElement]:
        """
        Get driver with depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            debug(f'Get element "{self.name}" from parent element "{self.parent.name}"')
            if wait:
                if isinstance(self, CoreElement):
                    self.wait_element(silent=True)
                else:
                    wait_page_loaded = getattr(self, 'wait_page_loaded')
                    wait_page_loaded(silent=True)

            base = self.parent._element

            if not base:
                base = self.parent.driver.find_element(self.parent.locator_type, self.parent.locator)

        return base

    def _get_wait(self, timeout=WAIT_EL) -> WebDriverWait:
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

    def _scaled_screenshot(self, screenshot_binary, width) -> Image:
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

    def _get_element(self, wait=True) -> SeleniumWebElement:
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
                raise NoSuchElementException(message) from NoSuchElementException

            try:
                if wait:
                    self.wait_element(silent=True)
                element = driver.find_element(self.locator_type, self.locator)
            except NoSuchElementException:
                message = f'Cant find element "{self.name}". {self.get_element_logging_data()}.'
                raise NoSuchElementException(message) from NoSuchElementException

        return element
