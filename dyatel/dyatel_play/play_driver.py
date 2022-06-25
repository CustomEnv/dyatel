from logging import info

from playwright.sync_api import Page as PlayPage
from playwright.sync_api import Browser


class PlayDriver:
    driver: Browser = None
    context: PlayPage = None

    def __init__(self, driver: Browser, initial_page=True):
        self.driver: Browser = driver

        if initial_page and not self.driver.contexts:
            self.context: PlayPage = self.driver.new_page()

        PlayDriver.driver = self.driver
        PlayDriver.context = self.context

    def get(self, url):
        """
        Navigate to given url

        :param url: url for navigation
        :return: self
        """
        info(f'Navigating to url {url}')
        self.context.goto(url)
        return self

    def is_driver_opened(self):
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        return self.driver.is_connected()

    def is_driver_closed(self):
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        return not self.driver.is_connected()

    @property
    def current_url(self):
        """
        Get current page url

        :return: url
        """
        return self.context.url

    def refresh(self):
        """
        Reload current page

        :return: self
        """
        info('Reload current page')
        self.context.reload()
        return self

    def go_forward(self):
        """
        Go forward by driver

        :return: self
        """
        info('Going forward')
        self.context.go_forward()
        return self

    def go_back(self):
        """
        Go back by driver

        :return: self
        """
        info('Going back')
        self.context.go_back()
        return self

    def quit(self, silent=True):
        """
        Quit the driver instance

        :param: silent:
        :return: self
        """
        if silent:
            info('Quit driver instance')

        self.driver.close()
        return self
