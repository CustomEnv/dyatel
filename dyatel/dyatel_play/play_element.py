import logging

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator


class PlayElement:
    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'
        self.parent = f'{parent}: parent does not supported for playwright'
        self.driver = PlayDriver.driver
        self.context = PlayDriver.context
        self.driver_wrapper = PlayDriver(self.driver, initial_page=False)

        self.child_elements = []
        for el in self._get_child_elements():
            if not el.driver:
                el.__init__(locator=el.locator, name=el.name)

    @property
    def element(self, *args, **kwargs):
        """ Get the current element by given locator """
        return self.context.locator(self.locator, *args, **kwargs)

    def click(self, *args, **kwargs):
        """ Click into element """
        logging.info(f'Click into "{self.name}"')
        self.element.click(*args, **kwargs)
        return self

    def get_text(self):
        """ Get element text """
        logging.info(f'Get text from "{self.name}"')
        return self.element.text_content()

    def is_displayed(self):
        """ Check visibility of element """
        logging.info(f'Check visibility of "{self.name}"')
        return self.element.is_visible()

    def is_hidden(self):
        """ Check if element hidden """
        logging.info(f'Check invisibility of "{self.name}"')
        return self.element.is_hidden()

    def wait_element(self):
        """ Wait for current element available in page """
        logging.info(f'Wait for presence of "{self.name}"')
        return self.element.wait_for(state='attached')

    def wait_element_hidden(self):
        """ Wait until element absence from page """
        logging.info(f'Wait for absence of "{self.name}"')
        return self.element.wait_for(state='hidden')

    def _get_child_elements(self):
        """Return page elements and page objects of this page object

        :returns: list of page elements and page objects
        """
        for attribute, value in list(self.__class__.__dict__.items()):
            if isinstance(value, PlayElement):
                self.child_elements.append(value)
        return self.child_elements
