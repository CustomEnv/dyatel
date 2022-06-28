from __future__ import annotations

from logging import info

from playwright.sync_api import Page as PlayPage
from playwright.sync_api import Browser


class PlayDriver:
    driver: Browser = None
    context: PlayPage = None

    mobile = False
    desktop = False
    is_ios = False
    is_android = False

    def __init__(self, driver: Browser, initial_page=True):
        """
        Initializing of desktop web driver with playwright

        :param initial_page: open new page right after connect with driver
        :param driver: playwright driver to initialize
        """
        self.driver = driver

        if initial_page and not self.driver.contexts:
            self.context: PlayPage = self.driver.new_page()

        PlayDriver.driver = self.driver
        PlayDriver.context = self.context
        PlayDriver.desktop = True

    def get(self, url) -> PlayDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :return: self
        """
        info(f'Navigating to url {url}')
        self.context.goto(url)
        return self

    def is_driver_opened(self) -> bool:
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        return self.driver.is_connected()

    def is_driver_closed(self) -> bool:
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        return not self.driver.is_connected()

    @property
    def current_url(self) -> str:
        """
        Get current page url

        :return: url
        """
        return self.context.url

    def refresh(self) -> PlayDriver:
        """
        Reload current page

        :return: self
        """
        info('Reload current page')
        self.context.reload()
        return self

    def go_forward(self) -> PlayDriver:
        """
        Go forward by driver

        :return: self
        """
        info('Going forward')
        self.context.go_forward()
        return self

    def go_back(self) -> PlayDriver:
        """
        Go back by driver

        :return: self
        """
        info('Going back')
        self.context.go_back()
        return self

    def quit(self, silent=True) -> PlayDriver:
        """
        Quit the driver instance

        :param: silent:
        :return: self
        """
        if silent:
            info('Quit driver instance')

        self.driver.close()
        return self
