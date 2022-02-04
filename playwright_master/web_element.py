import logging

from playwright_master.web_driver import WebDriver


class WebElement:
    def __init__(self, locator, name=None):
        self.driver = WebDriver.driver
        self.context = WebDriver.context
        self.locator = locator
        self.name = name
        if not name:
            self.name = self.locator

    def element(self, *args, **kwargs):
        return self.context.locator(self.locator, *args, **kwargs)

    def click(self, *args, **kwargs):
        logging.info(f'Click into "{self.name}"')
        self.element().click(*args, **kwargs)
        return self

    @property
    def get_text(self):
        logging.info(f'Get text from "{self.name}"')
        return self.element().text_content()

    def is_displayed(self):
        logging.info(f'Check visibility of "{self.name}"')
        return self.element().is_visible()

    def is_hidden(self):
        logging.info(f'Check invisibility of "{self.name}"')
        return self.element().is_hidden()

    def wait_element(self):
        logging.info(f'Wait for presence of "{self.name}"')
        return self.element().wait_for(state='attached')

    def wait_element_hidden(self):
        logging.info(f'Wait for absence of "{self.name}"')
        return self.element().wait_for(state='hidden')
