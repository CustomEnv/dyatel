from __future__ import annotations

import time
from abc import ABC
from typing import Union, List, Any

from PIL.Image import Image
from playwright.sync_api import TimeoutError as PlayTimeoutError
from playwright.sync_api import Page as PlaywrightPage
from playwright.sync_api import Locator, Page, Browser, BrowserContext

from dyatel.mixins.objects.size import Size
from dyatel.mixins.objects.location import Location
from dyatel.utils.selector_synchronizer import get_platform_locator, get_playwright_locator
from dyatel.abstraction.element_abc import ElementABC
from dyatel.exceptions import TimeoutException
from dyatel.utils.logs import Logging
from dyatel.shared_utils import cut_log_data, get_image
from dyatel.utils.internal_utils import (
    WAIT_EL,
    get_timeout_in_ms,
    calculate_coordinate_to_click,
    is_group,
    is_element,
)


class PlayElement(ElementABC, Logging, ABC):

    instance: Browser
    context: BrowserContext
    driver: Page
    parent: Union[ElementABC, PlayElement]
    _element: Locator = None

    def __init__(self, locator: str):  # noqa
        """
        Initializing of web element with playwright driver

        :param locator: anchor locator of page. Can be defined without locator_type
        """
        self.locator = get_playwright_locator(get_platform_locator(self))
        self.locator_type = 'locator_type does not supported for playwright'

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
            driver = self._get_base()
            element = driver.locator(self.locator)

        return element

    @element.setter
    def element(self, base_element: Union[Locator, None]):
        """
        Element object setter. Try to avoid usage of this function

        :param: play_element: playwright Locator object
        """
        self._element = base_element
    
    @property
    def all_elements(self) -> Union[list, List[Any]]:
        """
        Get all wrapped elements with playwright bases

        :return: list of wrapped objects
        """
        return self._get_all_elements(self.element.all())

    # Element interaction

    def click(self, force_wait: bool = True, *args, **kwargs) -> ElementABC:
        """
        Click to current element

        :param force_wait: wait for element visibility before click

        :param: args: https://playwright.dev/python/docs/api/class-locator#locator-click
        :param: kwargs: https://playwright.dev/python/docs/api/class-locator#locator-click
        :return: self
        """
        self.log(f'Click into "{self.name}"')

        if force_wait:
            self.wait_visibility(silent=True)

        self._first_element.click(*args, **kwargs)
        return self

    def click_outside(self, x: int = -5.0, y: int = -5.0) -> PlayElement:
        """
        Click outside of element. By default, 5px above and 5px left of element

        :param x: x offset of element to click
        :param y: y offset of element to click
        :return: self
        """
        self.log(f'Click outside from "{self.name}"')

        self._first_element.click(position={'x': x, 'y': y}, force=True)
        return self

    def click_into_center(self, silent: bool = False) -> PlayElement:
        """
        Click into the center of element

        :param silent: erase log message
        :return: self
        """
        if not self.is_fully_visible(silent=True):
            self.scroll_into_view()

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
            self.log(f'Type text "{cut_log_data(text)}" into "{self.name}"')

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

    def hover(self, silent: bool = False) -> PlayElement:
        """
        Hover over current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
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

    def check(self) -> PlayElement:
        """
        Check current checkbox

        :return: self
        """
        self._first_element.check()

        return self

    def uncheck(self) -> PlayElement:
        """
        Uncheck current checkbox

        :return: self
        """
        self._first_element.uncheck()

        return self

    # Element waits

    def wait_visibility(self, *, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait for current element available in page

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" becomes visible')

        try:
            self._first_element.wait_for(state='visible', timeout=get_timeout_in_ms(timeout))
        except PlayTimeoutError:
            raise TimeoutException(f'"{self.name}" not visible', timeout=timeout, info=self)
        return self

    def wait_hidden(self, *, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" becomes hidden')
        try:
            self._first_element.wait_for(state='hidden', timeout=get_timeout_in_ms(timeout))
        except PlayTimeoutError:
            raise TimeoutException(f'"{self.name}" still visible', timeout=timeout, info=self)
        return self

    def wait_availability(self, *, timeout: int = WAIT_EL, silent: bool = False) -> PlayElement:
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}"')

        try:
            self._first_element.wait_for(state='attached', timeout=get_timeout_in_ms(timeout))
        except PlayTimeoutError:
            raise TimeoutException(f'"{self.name}" not available in DOM', timeout=timeout, info=self)
        return self

    # Element state

    def scroll_into_view(
            self,
            sleep: Union[int, float] = 0,
            silent: bool = False,
            *args,  # noqa
            **kwargs,  # noqa
    ) -> PlayElement:
        """
        Scroll element into view

        :param: sleep: delay after scroll
        :param: silent: erase log
        :param: args: compatibility arg
        :param: kwargs: compatibility arg
        :return: self
        """
        if not silent:
            self.log(f'Scroll element "{self.name}" into view')

        self._first_element.scroll_into_view_if_needed()

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
        return get_image(screenshot_base)

    @property
    def screenshot_base(self) -> bytes:
        """
        Get screenshot binary of current element

        :return: screenshot binary
        """
        return self._first_element.screenshot()

    @property
    def text(self) -> str:
        """
        Get current element text

        :return: element text
        """
        element = self._first_element
        return element.text_content() if element.text_content() else element.input_value()

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

    def get_all_texts(self, silent: bool = False) -> List:
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

    @property
    def size(self) -> Size:
        """
        Get Size object of current element

        :return: Size(width/height) obj
        """
        box = self.element.first.bounding_box()
        return Size(width=box['width'], height=box['height'])

    @property
    def location(self) -> Location:
        """
        Get Location object of current element

        :return: Location(x/y) obj
        """
        box = self.element.first.bounding_box()
        return Location(x=box['x'], y=box['y'])

    def is_enabled(self, silent: bool = False) -> bool:
        """
        Check if element enabled

        :param silent: erase log
        :return: True if element enabled
        """
        if not silent:
            self.log(f'Check is element "{self.name}" enabled')

        return self._first_element.is_enabled()

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: bool
        """
        return self._first_element.is_checked()

    # Mixin

    def _get_base(self) -> Union[PlaywrightPage, Locator]:
        """
        Get driver depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            self.log(f'Get element "{self.name}" from parent element "{self.parent.name}"', level='debug')

            if is_group(self.parent) or is_element(self.parent):
                base = self.parent.element

        return base

    @property
    def _first_element(self):
        """
        Get first element

        :return: first element
        """
        return self.element.first
