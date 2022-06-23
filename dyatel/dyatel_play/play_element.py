from logging import info

from playwright.sync_api import Locator

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from dyatel.internal_utils import get_child_elements
from dyatel.utils import cut_log_data
from playwright._impl._api_types import TimeoutError as PlayTimeoutError


ELEMENT_WAIT = 10000


class PlayElement:
    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.parent = parent if parent else None
        self.driver = PlayDriver.driver
        self.context = PlayDriver.context
        self.driver_wrapper = PlayDriver(self.driver, initial_page=False)

        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'

        self.child_elements = get_child_elements(self, PlayElement)
        for el in self.child_elements:
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    # Element

    @property
    def element(self, *args, **kwargs) -> Locator:
        """
        Get playwright element

        :param args: args from Locator object
        :param kwargs: kwargs from Locator object
        :return: Locator
        """
        return self._get_driver().locator(self.locator, *args, **kwargs)

    @property
    def all_elements(self) -> list:
        """
        Get all playwright elements, matching given locator

        :return: list of elements
        """
        pass  # FIXME: implementation
        return []

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

        self.element.type(text=text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, silent=False):
        """
        Type text to current element slowly

        :param text: text to be slowly typed
        :param sleep_gap: sleep gap before each key press
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Type text {cut_log_data(text)} into "{self.name}"')

        self.element.type(text=text, delay=sleep_gap)
        return self

    def clear_text(self, silent=False):
        """
        Clear text from current element

        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Clear text in "{self.name}"')

        self.element.fill('')
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

        self.element.wait_for(state='attached', timeout=timeout)
        return self

    def wait_element_without_error(self, timeout=ELEMENT_WAIT, silent=False):
        """
        Wait for current element available in page without raising error

        :param timeout: time to stop waiting
        :param silent: erase log
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

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait hidden of "{self.name}"')

        self.element.wait_for(state='hidden', timeout=timeout)
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

        return self

    # Element state

    def get_text(self):
        """ Get element text """
        info(f'Get text from "{self.name}"')
        return self.element.text_content()

    def is_displayed(self):
        """ Check visibility of element """
        info(f'Check visibility of "{self.name}"')
        return self.element.is_visible()

    def is_hidden(self):
        """ Check if element hidden """
        info(f'Check invisibility of "{self.name}"')
        return self.element.is_hidden()

    def hover(self):
        """ Hover over self element """
        info(f'Hover over "{self.name}"')
        self.element.hover()
        return self

    @property
    def get_inner_text(self):
        return self.element.inner_text()

    @property
    def get_value(self):
        """ Get value from current element """
        return self.element.input_value()

    def click(self, *args, **kwargs):
        """ Click into element click """
        info(f'Click into "{self.name}"')
        self.element.click(*args, **kwargs)
        return self

    def click_outside(self, x=-5, y=-5):
        pass
        # FIXME: doesnt work
        # self.element.click(position={'x': x, 'y': y})

    def _get_driver(self):
        """
        Get driver including parent element if available
        """
        base = self.context
        if self.parent:
            base = self.parent.element
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base
