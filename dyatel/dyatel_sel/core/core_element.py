from __future__ import annotations

import time
from abc import ABC
from typing import Union, List, Any, Callable

from PIL import Image
from dyatel.mixins.objects.wait_result import Result
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    InvalidArgumentException as SeleniumInvalidArgumentException,
    InvalidSelectorException as SeleniumInvalidSelectorException,
    NoSuchElementException as SeleniumNoSuchElementException,
    ElementNotInteractableException as SeleniumElementNotInteractableException,
    ElementClickInterceptedException as SeleniumElementClickInterceptedException,
    StaleElementReferenceException as SeleniumStaleElementReferenceException,
)

from dyatel.abstraction.element_abc import ElementABC
from dyatel.dyatel_sel.sel_utils import ActionChains
from dyatel.js_scripts import get_element_size_js, get_element_position_on_screen_js
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.mixins.objects.location import Location
from dyatel.mixins.objects.scrolls import ScrollTo, ScrollTypes, scroll_into_view_blocks
from dyatel.mixins.objects.size import Size
from dyatel.shared_utils import cut_log_data, _scaled_screenshot
from dyatel.utils.internal_utils import WAIT_EL, safe_call, get_dict, HALF_WAIT_EL, wait_condition
from dyatel.exceptions import (
    TimeoutException,
    InvalidSelectorException,
    DriverWrapperException,
    NoSuchElementException,
    ElementNotInteractableException,
    NoSuchParentException,
)


class CoreElement(ElementABC, ABC):

    parent: Union[ElementABC, CoreElement]
    _element: Union[None, SeleniumWebElement, AppiumWebElement] = None
    _cached_element: Union[None, SeleniumWebElement, AppiumWebElement] = None

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium WebElement object

        :return: SeleniumWebElement
        """
        return self._get_element()

    @element.setter
    def element(self, base_element: Union[SeleniumWebElement, AppiumWebElement]):
        """
        Core element setter. Try to avoid usage of this function

        :param base_element: selenium WebElement or appium WebElement
        """
        self._element = base_element

    @property
    def all_elements(self) -> Union[None, List[Any]]:
        """
        Get all wrapped elements with selenium/appium bases

        :return: list of wrapped objects
        """
        return self._get_all_elements(self._find_elements())

    # Element interaction

    def click(self, force_wait: bool = True, *args, **kwargs) -> CoreElement:
        """
        Click to current element

        :param force_wait: wait for element visibility before click
        :param args: compatibility arg.
        :param kwargs: compatibility arg.
        :return: self
        """
        self.log(f'Click into "{self.name}"')

        self.element = self._get_element(force_wait=force_wait)

        selenium_exc_msg = None
        start_time = time.time()
        while time.time() - start_time < HALF_WAIT_EL:
            try:
                self.wait_enabled(silent=True).element.click()
                return self
            except (
                    SeleniumElementNotInteractableException,
                    SeleniumElementClickInterceptedException,
                    SeleniumStaleElementReferenceException,
            ) as exc:
                selenium_exc_msg = exc.msg
            finally:
                self.element = None

        raise ElementNotInteractableException(
            f'Element "{self.name}" not interactable after {HALF_WAIT_EL} seconds. {self.get_element_info()}. '
            f'Original error: {selenium_exc_msg}'
        )

    def type_text(self, text: Union[str, KeyboardKeys], silent: bool = False) -> CoreElement:
        """
        Type text to current element

        :param text: text to be typed
        :param silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            self.log(f'Type text "{cut_log_data(text)}" into "{self.name}"')

        self.element.send_keys(text)
        return self

    def type_slowly(self, text: str, sleep_gap: float = 0.05, silent: bool = False) -> CoreElement:
        """
        Type text to current element slowly

        :param text: text to be slowly typed
        :param sleep_gap: sleep gap before each key press
        :param silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            self.log(f'Type text "{cut_log_data(text)}" into "{self.name}"')

        element = self.element
        for letter in str(text):
            element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, silent: bool = False) -> CoreElement:
        """
        Clear text from current element

        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Clear text in "{self.name}"')

        self.element.clear()
        return self

    def check(self) -> CoreElement:
        """
        Check current checkbox

        :return: self
        """
        self.element = self._get_element(wait=self.wait_availability)

        try:
            if not self.is_checked():
                self.click(with_wait=False)
        finally:
            self.element = None

        return self

    def uncheck(self) -> CoreElement:
        """
        Uncheck current checkbox

        :return: self
        """
        self.element = self._get_element(wait=self.wait_availability)

        try:
            if self.is_checked():
                self.click(with_wait=False)
        finally:
            self.element = None

        return self

    # Element waits

    @wait_condition
    def wait_visibility(self, *, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in page

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        return Result(  # noqa
            execution_result=self.is_displayed(silent=True),
            log=f'Wait until "{self.name}" becomes visible',
            exc=TimeoutException(f'"{self.name}" not visible', info=self)
        )

    @wait_condition
    def wait_hidden(self, *, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element hidden

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        return Result(  # noqa
            execution_result=self.is_hidden(silent=True),
            log=f'Wait until "{self.name}" becomes hidden',
            exc=TimeoutException(f'"{self.name}" still visible', info=self),
        )

    @wait_condition
    def wait_availability(self, *, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in DOM

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        return Result(  # noqa
            execution_result=self.is_available(),
            log=f'Wait until presence of "{self.name}"',
            exc=TimeoutException(f'"{self.name}" not available in DOM', info=self),
        )

    # Element state

    def scroll_into_view(
            self,
            block: ScrollTo = ScrollTo.CENTER,
            behavior: ScrollTypes = ScrollTypes.INSTANT,
            sleep: Union[int, float] = 0,
            silent: bool = False,
    ) -> CoreElement:
        """
        Scroll element into view by js script

        :param block: start - element on the top; end - element at the bottom. All types in ScrollTo object
        :param behavior: scroll type: ScrollTypes.INSTANT or ScrollTypes.SMOOTH
        :param sleep: delay after scroll
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Scroll element "{self.name}" into view')

        assert block in scroll_into_view_blocks, f'Provide one of {scroll_into_view_blocks} option in `block` argument'

        self.execute_script(f'arguments[0].scrollIntoView({{block: "{block}", behavior: "{behavior}"}});')

        if sleep:
            time.sleep(sleep)

        return self

    def screenshot_image(self, screenshot_base: bytes = None) -> Image:
        """
        Get PIL Image object with scaled screenshot of current element

        :param screenshot_base: screenshot bytes
        :return: PIL Image object
        """
        screenshot_base = screenshot_base if screenshot_base else self.screenshot_base
        return _scaled_screenshot(screenshot_base, self.size.width)

    @property
    def screenshot_base(self) -> bytes:
        """
        Get screenshot binary of current element

        :return: screenshot binary
        """
        return self.element.screenshot_as_png

    @property
    def text(self) -> str:
        """
        Get text from current element

        :return: element text
        """
        element = self._get_element(wait=self.wait_availability)
        return element.text

    @property
    def inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        return self.get_attribute('textContent', silent=True) or self.get_attribute('innerText', silent=True)

    @property
    def value(self) -> str:
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
        element = safe_call(self._find_element, wait_parent=False)

        return bool(element)

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of element

        :param silent: erase log
        :return: True if element visible
        """
        if not silent:
            self.log(f'Check displaying of "{self.name}"')

        is_displayed = self.is_available()

        if is_displayed:
            is_displayed = safe_call(self._cached_element.is_displayed)

        return is_displayed

    def is_hidden(self, silent: bool = False) -> bool:
        """
        Check invisibility of current element

        :param silent: erase log
        :return: True if element hidden
        """
        if not silent:
            self.log(f'Check invisibility of "{self.name}"')

        return not self.is_displayed(silent=True)

    def get_attribute(self, attribute: str, silent: bool = False) -> str:
        """
        Get custom attribute from current element

        :param attribute: custom attribute: value, innerText, textContent etc.
        :param silent: erase log
        :return: custom attribute value
        """
        if not silent:
            self.log(f'Get "{attribute}" from "{self.name}"')

        return self.element.get_attribute(attribute)

    def get_all_texts(self, silent: bool = False) -> List[str]:
        """
        Get all texts from all matching elements

        :param silent: erase log
        :return: list of texts
        """
        if not silent:
            self.log(f'Get all texts from "{self.name}"')

        self.wait_visibility(silent=True)
        return list(element_item.text for element_item in self.all_elements)

    def get_elements_count(self, silent: bool = False) -> int:
        """
        Get elements count

        :param silent: erase log
        :return: elements count
        """
        if not silent:
            self.log(f'Get elements count of "{self.name}"')

        return len(self.all_elements)

    def get_rect(self) -> dict:
        """
        A dictionary with the size and location of the element.

        :return: dict ~ {'y': 0, 'x': 0, 'width': 0, 'height': 0}
        """
        sorted_items = sorted({**get_dict(self.size), **get_dict(self.location)}.items(), reverse=True)
        return dict(sorted_items)

    @property
    def size(self) -> Size:
        """
        Get Size object of current element

        :return: Size(width/height) obj
        """
        return Size(**self.execute_script(get_element_size_js))

    @property
    def location(self) -> Location:
        """
        Get Location object of current element

        :return: Location(x/y) obj
        """
        return Location(**self.execute_script(get_element_position_on_screen_js))

    def is_enabled(self, silent: bool = False) -> bool:
        """
        Check if element enabled

        :param silent: erase log
        :return: True if element enabled
        """
        if not silent:
            self.log(f'Check is element "{self.name}" enabled')

        return self.element.is_enabled()

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: bool
        """
        return self._get_element(wait=self.wait_availability).is_selected()

    # Mixin

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

    def _get_element(self, wait: Union[bool, Callable] = True, force_wait: bool = False) -> SeleniumWebElement:
        """
        Get selenium element from driver or parent element

        :param wait: wait strategy for element and/or element parent before grab
        :param force_wait: force wait for some element
        :return: SeleniumWebElement
        """
        element = self._element

        if wait is True:
            wait = self.wait_visibility

        if not element:

            # Try to get element instantly without wait. Skipped if force_wait given
            if not force_wait:
                element = safe_call(self._find_element, wait_parent=False)

            # Wait for element if it is not found instantly
            if (not element and wait) or force_wait:
                element = self._get_cached_element(safe_call(wait, silent=True))

        if not element:
            if self.parent and not self._get_cached_element(self.parent):
                raise NoSuchParentException(
                    f'Cant find parent object "{self.parent.name}". {self.get_element_info(self.parent)}'  # noqa
                )

            raise NoSuchElementException(
                f'Cant find element "{self.name}". {self.get_element_info()}{self._ensure_unique_parent()}'
            )

        return element

    def _get_base(self, wait: Union[bool, Callable] = True) -> Union[SeleniumWebDriver, SeleniumWebElement]:
        """
        Get driver with depends on parent element if available

        :return: driver
        """
        base = self.driver

        if not base:
            raise DriverWrapperException("Can't find driver")

        if self.driver_wrapper.is_appium:
            if self.driver_wrapper.is_native_context:
                return base

        if self.parent:
            base = self.parent._get_element(wait=wait)

        return base

    def _find_element(self, wait_parent: bool = False) -> Union[SeleniumWebElement, AppiumWebElement]:
        """
        Find selenium/appium element

        :param wait_parent: wait for base(parent) element
        :return: SeleniumWebElement or AppiumWebElement
        """
        base = self._get_base(wait=wait_parent)
        self._cached_element = None

        try:
            element = base.find_element(self.locator_type, self.locator)
            self._cached_element = element
            return element
        except (SeleniumInvalidArgumentException, SeleniumInvalidSelectorException) as exc:
            self._raise_invalid_selector_exception(exc)
        except SeleniumNoSuchElementException as exc:
            raise NoSuchElementException(exc.msg)

    def _find_elements(self, wait_parent: bool = False) -> List[Union[SeleniumWebElement, AppiumWebElement]]:
        """
        Find all selenium/appium elements

        :param wait_parent: wait for base(parent) element
        :return: list of SeleniumWebElement or AppiumWebElement
        """
        base = self._get_base(wait=wait_parent)
        self._cached_element = None

        try:
            elements = base.find_elements(self.locator_type, self.locator)

            if elements:
                self._cached_element = elements[0]

            return elements
        except (SeleniumInvalidArgumentException, InvalidSelectorException) as exc:
            self._raise_invalid_selector_exception(exc)

    def _raise_invalid_selector_exception(self, exc: Any) -> None:
        """
        Raises InvalidSelectorException if specific keywords in exception message

        :param exc: original exc object
        :return: None
        """
        if 'invalid locator' in exc.msg or 'is not a valid' in exc.msg:
            msg = f'Selector for "{self.name}" is invalid. {self.get_element_info()}'
            raise InvalidSelectorException(msg)
        else:
            raise exc

    def _ensure_unique_parent(self) -> str:
        """
        Ensure that parent is unique and give information if it isn't

        :return: empty string or warning info
        """
        info = ''
        if self.parent:
            parents_count = len(self.parent._find_elements())
            if parents_count > 1:
                info = f'\nWARNING: The parent object is not unique, count of parent elements are: {parents_count}'

        return info

    def _get_cached_element(self, obj: CoreElement) -> Union[None, SeleniumWebElement, AppiumWebElement]:
        """
        Get cached element from given object

        :param obj: CoreElement object
        :return: None, SeleniumWebElement, AppiumWebElement
        """
        return getattr(obj, '_cached_element', None)
