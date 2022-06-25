from logging import info
from typing import Union

from playwright.sync_api import Locator

# noinspection PyProtectedMember
from playwright._impl._api_types import TimeoutError as PlayTimeoutError
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from dyatel.internal_utils import get_child_elements, get_timeout
from playwright.sync_api import Page as PlayPage
from dyatel.shared_utils import cut_log_data


ELEMENT_WAIT = get_timeout(10)


class PlayElement:

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.parent = parent if parent else None
        self.driver = PlayDriver.driver
        self.context = PlayDriver.context
        self.driver_wrapper = PlayDriver(self.driver, initial_page=False)

        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'
        self._element = None

        self.child_elements = get_child_elements(self, PlayElement)
        for el in self.child_elements:
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    # Element

    @property
    def element(self, *args, **kwargs) -> Locator:
        """
        Get playwright element

        :param: args: args from Locator object
        :param: kwargs: kwargs from Locator object
        :return: Locator
        """
        return self._element if self._element else self._get_driver().locator(self.locator, *args, **kwargs)

    @element.setter
    def element(self, play_element):
        """
        Current class element setter. Try to avoid usage of this function

        :param: play_element: playwright Locator object, that will be set for current class
        """
        self._element = play_element
    
    @property
    def all_elements(self) -> list:
        """
        Get all PlayElement elements, matching given locator

        :return: list of elements
        """
        wrapped_elements = []
        for element in self.element.element_handles():
            wrapped_object = PlayElement(self.locator, self.locator_type, self.name, self.parent)
            wrapped_object.element = element
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    # Element interaction

    def click(self, *args, **kwargs):
        """
        Click to current element

        :param: args: https://playwright.dev/python/docs/api/class-locator#locator-click
        :param: kwargs: https://playwright.dev/python/docs/api/class-locator#locator-click
        :return: self
        """
        info(f'Click into "{self.name}"')
        self.element.click(*args, **kwargs)
        return self

    def click_outside(self, x=-5.0, y=-5.0):
        """
        Click outside of element. By default, 5px above and 5px left of element

        :param: x: x offset
        :param: y: y offset
        :return: self
        """
        self.element.click(position={'x': x, 'y': y}, force=True)
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

        self.element.type(text=text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, silent=False):
        """
        Type text to current element slowly

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')

        self.element.type(text=text, delay=sleep_gap)
        return self

    def clear_text(self, silent=False):
        """
        Clear text from current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Clear text in "{self.name}"')

        self.element.fill('')
        return self

    def hover(self):
        """
        Hover over current element

        :return: self
        """
        info(f'Hover over "{self.name}"')
        self.element.hover()
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

        self.element.wait_for(state='attached', timeout=get_timeout(timeout))
        self.element.wait_for(state='visible', timeout=get_timeout(timeout))
        return self

    def wait_element_without_error(self, timeout=ELEMENT_WAIT, silent=False):
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

    def wait_element_hidden(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait hidden of "{self.name}"')

        self.element.wait_for(state='hidden', timeout=get_timeout(timeout))
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
            info(f'Skip wait until clickable of "{self.name}". Timeout: {timeout}')

        return self

    # Element state

    def get_text(self):
        """
        Get current element text

        :return: element text
        """
        info(f'Get text from "{self.name}"')
        return self.element.text_content()

    @property
    def get_inner_text(self):
        """
        Get current element inner text

        :return: element inner text
        """
        return self.element.inner_text()

    @property
    def get_value(self):
        """
        Get value from current element

        :return: element value
        """
        return self.element.input_value()

    def is_available(self):
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        return bool(len(self.all_elements))

    def is_displayed(self):
        """
        Check visibility of current element

        :return: True if element visible
        """
        info(f'Check visibility of "{self.name}"')
        return self.element.is_visible()

    def is_hidden(self):
        """
        Check invisibility of current element

        :return: True if element hidden
        """
        info(f'Check invisibility of "{self.name}"')
        return self.element.is_hidden()

    def get_attribute(self, attribute, silent=False):
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            info(f'Get "{attribute}" from "{self.name}"')

        return self.element.get_attribute(attribute)

    def get_elements_texts(self, silent=False) -> list:
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

    def _get_driver(self) -> Union[PlayPage, Locator]:
        """
        Get driver depends on parent element if available

        :return: driver
        """
        base = self.context
        if self.parent:
            base = self.parent.element
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base
