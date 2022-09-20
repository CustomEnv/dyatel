from __future__ import annotations

import time
from typing import Union, List, Any

# noinspection PyProtectedMember
from playwright._impl._api_types import TimeoutError as PlayTimeoutError

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from playwright.sync_api import Page as PlaywrightPage, ElementHandle
from playwright.sync_api import Locator
from dyatel.mixins.log_mixin import LogMixin
from dyatel.shared_utils import cut_log_data
from dyatel.mixins.element_mixin import ElementMixin
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.internal_utils import get_child_elements, WAIT_EL, get_timeout_in_ms, initialize_objects_with_args, \
    calculate_coordinate_to_click


class PlayElement(ElementMixin, DriverMixin, LogMixin):

    def __init__(self, locator: str, locator_type: str = '', name: str = '',
                 parent: Union[PlayElement, Any] = None, wait: bool = False):
        """
        Initializing of web element with playwright driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: compatibility arg - specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be PlayElement, PlayPage, Group objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self._element = None
        self._initialized = True
        self._driver_instance = PlayDriver

        self.locator = get_selenium_completable_locator(locator)
        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'
        self.name = name if name else self.locator
        self.wait = wait
        self.parent: Union[PlayElement, Any] = parent if parent else None

        self.child_elements: List[PlayElement] = get_child_elements(self, PlayElement)
        initialize_objects_with_args(self.child_elements)

    # Element

    @property
    def element(self) -> Locator:
        """
        Get playwright Locator object

        :param: args: args from Locator object
        :param: kwargs: kwargs from Locator object
        :return: Locator
        """
        element = self._element
        if not element:

            driver = self._get_driver()
            if isinstance(driver, ElementHandle):
                element = driver.query_selector(self.locator)
            else:
                element = driver.locator(self.locator)

        return element

    @element.setter
    def element(self, play_element: Locator):
        """
        Current class element setter. Try to avoid usage of this function

        :param: play_element: playwright Locator object, that will be set for current class
        """
        self._element = play_element
    
    @property
    def all_elements(self) -> List[Any]:
        """
        Get all wrapped elements with playwright bases

        :return: list of wrapped objects
        """
        return self._get_all_elements(self.element.element_handles(), PlayElement)

    # Element interaction

    def click(self, *args, **kwargs) -> PlayElement:
        """
        Click to current element

        :param: args: https://playwright.dev/python/docs/api/class-locator#locator-click
        :param: kwargs: https://playwright.dev/python/docs/api/class-locator#locator-click
        :return: self
        """
        self.log(f'Click into "{self.name}"')
        self._first_element.click(*args, **kwargs)
        return self

    def click_outside(self, x: int = -5.0, y: int = -5.0) -> PlayElement:
        """
        Click outside of element. By default, 5px above and 5px left of element

        :param: x: x offset
        :param: y: y offset
        :return: self
        """
        self._first_element.click(position={'x': x, 'y': y}, force=True)
        return self

    def click_into_center(self, silent: bool = False) -> PlayElement:
        """
        Click into the center of element

        :param silent: erase log message
        :return: self
        """
        x, y = calculate_coordinate_to_click(self, 0, 0)

        if not silent:
            self.log(f'Click into the center (x: {x}, y: {y}) for "{self.name}"')

        self.driver_wrapper.click_by_coordinates(x=x, y=y, silent=True)
        return self

    def type_text(self, text: str, silent: bool = False) -> PlayElement:
        """
        Type text to current element

        :param: text: text to be typed
        :param: silent: erase log
        :return: self
        """
        text = str(text)
        if not silent:
            self.log(f'Type text {cut_log_data(text)} into "{self.name}"')

        self._first_element.type(text=text)
        return self

    def type_slowly(self, text: str, sleep_gap: float = 0.05, silent: bool = False) -> PlayElement:
        """
        Type text to current element slowly

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Type text {cut_log_data(text)} into "{self.name}"')

        self._first_element.type(text=text, delay=sleep_gap)
        return self

    def clear_text(self, silent: bool = False) -> PlayElement:
        """
        Clear text from current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Clear text in "{self.name}"')

        self._first_element.fill('')
        return self

    def hover(self) -> PlayElement:
        """
        Hover over current element

        :return: self
        """
        self.log(f'Hover over "{self.name}"')
        self._first_element.hover()
        return self

    def hover_outside(self, x: int = 0, y: int = -5) -> PlayElement:
        """
        Hover outside from current element

        :return: self
        """
        self.log(f'Hover outside from "{self.name}"')
        self._first_element.hover(position={'x': float(x), 'y': float(y)}, force=True)
        return self

    # Element waits

    def wait_element(self, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait for current element available in page

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}"')

        self._first_element.wait_for(state='visible', timeout=get_timeout_in_ms(timeout))
        return self

    def wait_element_without_error(self, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait for current element available in page without raising error

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except PlayTimeoutError as exception:
            self.log(f'Ignored exception: "{exception}"')
        return self

    def wait_element_hidden(self, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait hidden of "{self.name}"')

        self._first_element.wait_for(state='hidden', timeout=get_timeout_in_ms(timeout))
        return self

    def wait_clickable(self, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Compatibility placeholder
        Wait until element clickable

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Skip wait until clickable of "{self.name}". Timeout: {timeout}')

        return self

    def wait_availability(self, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}"')

        self._first_element.wait_for(state='attached', timeout=get_timeout_in_ms(timeout))
        return self

    # Element state

    def scroll_into_view(self, sleep: Union[int, float] = 0) -> PlayElement:
        """
        Scroll element into view

        :param sleep: delay after scroll
        :return: self
        """
        self.log(f'Scroll element "{self.name}" into view')
        self._first_element.scroll_into_view_if_needed()

        if sleep:
            time.sleep(sleep)

        return self

    def get_screenshot(self, filename: str) -> bytes:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :return: image binary
        """
        self.log(f'Get screenshot of "{self.name}"')
        return self._first_element.screenshot(path=filename)

    @property
    def screenshot_base(self) -> bytes:
        """
        Get driver width scaled screenshot binary of element without saving

        :return: screenshot binary
        """
        return self._first_element.screenshot()

    @property
    def text(self) -> str:
        """
        Get current element text

        :return: element text
        """
        self.log(f'Get text from "{self.name}"')
        return self._first_element.text_content()

    @property
    def inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        return self._first_element.inner_text()

    @property
    def value(self) -> str:
        """
        Get value from current element

        :return: element value
        """
        return self._first_element.input_value()

    def is_available(self) -> bool:
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        return bool(len(self.element.element_handles()))

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of current element

        :param: silent: erase log
        :return: True if element visible
        """
        if not silent:
            self.log(f'Check visibility of "{self.name}"')

        return self._first_element.is_visible()

    def is_hidden(self, silent: bool = False) -> bool:
        """
        Check invisibility of current element

        :param: silent: erase log
        :return: True if element hidden
        """
        if not silent:
            self.log(f'Check invisibility of "{self.name}"')

        return self._first_element.is_hidden()

    def get_attribute(self, attribute: str, silent: bool = False) -> str:
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            self.log(f'Get "{attribute}" from "{self.name}"')

        return self._first_element.get_attribute(attribute)

    def get_elements_texts(self, silent: bool = False) -> List:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            self.log(f'Get all texts from "{self.name}"')

        return self.element.all_text_contents()

    def get_elements_count(self, silent: bool = False) -> int:
        """
        Get elements count

        :param: silent: erase log
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
        sorted_items: list = sorted(self.element.bounding_box().items(), reverse=True)
        return dict(sorted_items)

    # Mixin

    def _get_driver(self) -> Union[PlaywrightPage, Locator, ElementHandle]:
        """
        Get driver depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            self.log(f'Get element "{self.name}" from parent element "{self.parent.name}"', level='debug')

            if isinstance(self.parent, PlayElement):
                base = self.parent.element
            else:
                base = self.parent.anchor.element

        return base

    @property
    def _first_element(self):
        """
        Get first element

        :return: first element
        """
        return self.element if isinstance(self.element, ElementHandle) else self.element.first
