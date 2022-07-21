from __future__ import annotations

import time
from logging import info, debug
from typing import Union, List, Any

# noinspection PyProtectedMember
from playwright._impl._api_types import TimeoutError as PlayTimeoutError

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from playwright.sync_api import Page as PlaywrightPage, ElementHandle
from playwright.sync_api import Locator
from dyatel.shared_utils import cut_log_data
from dyatel.internal_utils import (
    get_child_elements,
    Mixin,
    WAIT_EL,
    get_timeout_in_ms,
    initialize_objects_with_args,
    DriverMixin,
)


class PlayElement(Mixin, DriverMixin):

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False):
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
        self.name = name if name else self.locator
        self.wait = wait
        self.parent: Union[PlayElement, Any] = parent if parent else None
        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'

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
    def element(self, play_element):
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
        info(f'Click into "{self.name}"')
        self._first_element.click(*args, **kwargs)
        return self

    def click_outside(self, x=-5.0, y=-5.0) -> PlayElement:
        """
        Click outside of element. By default, 5px above and 5px left of element

        :param: x: x offset
        :param: y: y offset
        :return: self
        """
        self._first_element.click(position={'x': x, 'y': y}, force=True)
        return self

    def type_text(self, text, silent=False) -> PlayElement:
        """
        Type text to current element

        :param: text: text to be typed
        :param: silent: erase log
        :return: self
        """
        text = str(text)
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')

        self._first_element.type(text=text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, silent=False) -> PlayElement:
        """
        Type text to current element slowly

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')

        self._first_element.type(text=text, delay=sleep_gap)
        return self

    def clear_text(self, silent=False) -> PlayElement:
        """
        Clear text from current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Clear text in "{self.name}"')

        self._first_element.fill('')
        return self

    def hover(self) -> PlayElement:
        """
        Hover over current element

        :return: self
        """
        info(f'Hover over "{self.name}"')
        self._first_element.hover()
        return self

    # Element waits

    def wait_element(self, timeout=WAIT_EL, silent=False) -> PlayElement:
        """
        Wait for current element available in page

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}"')

        self._first_element.wait_for(state='attached', timeout=get_timeout_in_ms(timeout))
        self._first_element.wait_for(state='visible', timeout=get_timeout_in_ms(timeout))
        return self

    def wait_element_without_error(self, timeout=WAIT_EL, silent=False) -> PlayElement:
        """
        Wait for current element available in page without raising error

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}" without error exception')

        try:
            self.wait_element(timeout=timeout, silent=True)
        except PlayTimeoutError as exception:
            info(f'Ignored exception: "{exception}"')
        return self

    def wait_element_hidden(self, timeout=WAIT_EL, silent=False) -> PlayElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait hidden of "{self.name}"')

        self._first_element.wait_for(state='hidden', timeout=get_timeout_in_ms(timeout))
        return self

    def wait_clickable(self, timeout=WAIT_EL, silent=False) -> PlayElement:
        """
        Compatibility placeholder
        Wait until element clickable

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Skip wait until clickable of "{self.name}". Timeout: {timeout}')

        return self

    # Element state

    def scroll_into_view(self, sleep=0) -> PlayElement:
        """
        Scroll element into view

        :return: self
        """
        info(f'Scroll element "{self.name}" into view')
        self._first_element.scroll_into_view_if_needed()

        if sleep:
            time.sleep(sleep)

        return self

    def get_screenshot(self, filename) -> bytes:  # TODO: research
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :return: image binary
        """
        info(f'Get screenshot of "{self.name}"')
        return self._first_element.screenshot(path=filename)

    @property
    def get_screenshot_base(self) -> bytes:  # TODO: research
        """
        Get driver width scaled screenshot binary of element without saving

        :return: screenshot binary
        """
        return self._first_element.screenshot()

    @property
    def get_text(self) -> str:
        """
        Get current element text

        :return: element text
        """
        info(f'Get text from "{self.name}"')
        return self._first_element.text_content()

    @property
    def get_inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        return self._first_element.inner_text()

    @property
    def get_value(self) -> str:
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

    def is_displayed(self, silent=False) -> bool:
        """
        Check visibility of current element

        :param: silent: erase log
        :return: True if element visible
        """
        if not silent:
            info(f'Check visibility of "{self.name}"')

        return self._first_element.is_visible()

    def is_hidden(self, silent=False) -> bool:
        """
        Check invisibility of current element

        :param: silent: erase log
        :return: True if element hidden
        """
        if not silent:
            info(f'Check invisibility of "{self.name}"')

        return self._first_element.is_hidden()

    def get_attribute(self, attribute, silent=False) -> str:
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')

        return self._first_element.get_attribute(attribute)

    def get_elements_texts(self, silent=False) -> List:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            info(f'Get all texts from "{self.name}"')

        return self.element.all_text_contents()

    def get_elements_count(self, silent=False) -> int:
        """
        Get elements count

        :param: silent: erase log
        :return: elements count
        """
        if not silent:
            info(f'Get elements count of "{self.name}"')

        return len(self.all_elements)

    # Mixin

    def _get_driver(self) -> Union[PlaywrightPage, Locator, ElementHandle]:
        """
        Get driver depends on parent element if available

        :return: driver
        """
        base = self.driver
        if self.parent:
            debug(f'Get element "{self.name}" from parent element "{self.parent.name}"')

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
