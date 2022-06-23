import logging
import os

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from dyatel.internal_utils import get_child_elements


class PlayPage:

    def __init__(self, locator, locator_type=None, name=None):
        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.locator_type = f'{locator_type}: locator_type does not supported for playwright'
        self.driver = PlayDriver.driver
        self.context = PlayDriver.context
        self.driver_wrapper = PlayDriver(self.driver, initial_page=False)

        self.url = getattr(self, 'url', '')
        self.page_elements = get_child_elements(self, PlayElement)
        for el in self.page_elements:
            if not el.driver:
                el.__init__(locator=el.locator, locator_type=el.locator_type, name=el.name, parent=el.parent)

    def open_page(self, url=''):
        url = self.url if not url else url
        self.driver_wrapper.get(url)
        return self

    def get(self, url, *args, **kwargs):
        """ Navigate to page and wait until loaded """
        sensitive_url = url.replace(os.getcwd(), '****') if os.getcwd() in url else url
        logging.info(f'Go to url {sensitive_url}')
        self.context.goto(url, *args, **kwargs)
        self.wait_until_opened()
        return self

    def wait_until_opened(self):
        """ Wait until page loaded """
        logging.info(f'Wait until page opened {self.name}')
        self.context.wait_for_selector(self.locator)
        return self

    def refresh(self):
        """ Reload current page """
        logging.info('Reload current page')
        self.context.reload()
        return self

    def go_forward(self):
        """ Go forward """
        logging.info('Going forward')
        self.context.go_forward()
        return self

    def go_back(self):
        """ Go back """
        logging.info('Going back')
        self.context.go_back()
        return self
