from typing import Union

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver


class Driver(WebDriver, MobileDriver, PlayDriver):
    """ Driver object crossroad """

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumWebDriver]):
        """
        Initializing of driver wrapper based on given driver source

        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.__set_driver_class()
        super().__init__(driver=driver)

    def __set_driver_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class

        :return: driver wrapper class
        """
        if isinstance(self.driver, PlaywrightDriver):
            Driver.__bases__ = PlayDriver,
            return PlayDriver
        if isinstance(self.driver, AppiumDriver):
            Driver.__bases__ = MobileDriver,
            return MobileDriver
        if isinstance(self.driver, SeleniumWebDriver):
            Driver.__bases__ = WebDriver,
            return WebDriver
        else:
            raise Exception('Cant specify Driver')
