from __future__ import annotations

from typing import Union
from logging import info

from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver


class CoreDriver:
    driver: Union[AppiumDriver, SeleniumWebDriver] = None

    mobile = False
    desktop = False
    is_ios = False
    is_android = False

    def __init__(self, driver: Union[AppiumDriver, SeleniumWebDriver]):
        """
        Initializing of core driver
        Contain same methods/data for both WebDriver and MobileDriver classes

        :param driver: appium or selenium driver to initialize
        """
        self.driver = driver

    def get(self, url) -> CoreDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :return: self
        """
        info(f'Navigating to url {url}')
        self.driver.get(url)
        return self

    def is_driver_opened(self) -> bool:
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        return True if self.driver else False

    def is_driver_closed(self) -> bool:
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        return False if self.driver else True

    @property
    def current_url(self) -> str:
        """
        Get current page url

        :return: url
        """
        return self.driver.current_url

    def refresh(self) -> CoreDriver:
        """
        Reload current page

        :return: self
        """
        info('Reload current page')
        self.driver.refresh()
        return self

    def go_forward(self) -> CoreDriver:
        """
        Go forward by driver

        :return: self
        """
        info('Going forward')
        self.driver.forward()
        return self

    def go_back(self) -> CoreDriver:
        """
        Go back by driver

        :return: self
        """
        info('Going back')
        self.driver.back()
        return self

    def quit(self, silent=True) -> CoreDriver:
        """
        Quit the driver instance

        :param: silent:
        :return: self
        """
        if silent:
            info('Quit driver instance')

        self.driver.close()
        self.driver.quit()
        return self
