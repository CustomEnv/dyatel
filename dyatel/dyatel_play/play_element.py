from logging import info

from playwright.sync_api import Locator

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from dyatel.utils import cut_log_data

ELEMENT_WAIT = 10


class PlayElement:
    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.parent = parent if parent else None
        self.driver = PlayDriver.driver
        self.context = PlayDriver.context
        self.driver_wrapper = PlayDriver(self.driver, initial_page=False)

        self.child_elements = []
        for el in self._get_child_elements():
            if not el.driver:
                el.__init__(locator=el.locator, name=el.name)

        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'

    @property
    def element(self, *args, **kwargs) -> Locator:
        """ Get the current element by given locator """
        return self._get_driver().locator(self.locator, *args, **kwargs)

    def click(self, *args, **kwargs):
        """ Click into element """
        info(f'Click into "{self.name}"')
        self.element.click(*args, **kwargs)
        return self

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

    def wait_element(self):
        """ Wait for current element available in page """
        info(f'Wait for presence of "{self.name}"')
        self.element.wait_for(state='attached')
        return self

    def wait_element_without_error(self, timeout=ELEMENT_WAIT):
        """ Wait for current element available in page """
        # Compatibility placeholder
        return self

    def wait_element_hidden(self):
        """ Wait until element absence from page """
        info(f'Wait for absence of "{self.name}"')
        self.element.wait_for(state='hidden')
        return self

    def hover(self):
        """ Hover over self element """
        info(f'Hover over "{self.name}"')
        self.element.hover()
        return self

    def type_text(self, text):
        """ Type text to current element """
        info(f'Type text {cut_log_data(text)} into "{self.name}"')
        self.element.type(text=text)
        return self

    def clear_text(self):
        """ Clear text from current element """
        self.element.type(text='')
        return self

    def get_value(self):
        """ Type text to current element """
        self.element.get_attribute('value')
        return self

    def click_outside1(self, x=-5, y=-5):
        self.element.click(position={'x': x, 'y': y})

    def _get_driver(self):
        """
        Get driver including parent element if available
        """
        base = self.context
        if self.parent:
            base = self.parent.element
            info(f'Get element "{self.name}" from parent element "{self.parent.name}"')
        return base

    def _get_child_elements(self):
        """Return page elements and page objects of this page object

        :returns: list of page elements and page objects
        """
        for attribute, value in list(self.__class__.__dict__.items()):
            if isinstance(value, PlayElement):
                self.child_elements.append(value)
        return self.child_elements
