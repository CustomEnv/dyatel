from typing import Union

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException


class DriverWrapper(WebDriver, MobileDriver, PlayDriver):
    """ Driver object crossroad """

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumDriver]):
        """
        Initializing of driver wrapper based on given driver source

        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.__set_base_class()
        super().__init__(driver=driver)

    def __set_base_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class

        :return: driver wrapper class
        """
        if isinstance(self.driver, PlaywrightDriver):
            DriverWrapper.__bases__ = PlayDriver,
            return PlayDriver
        if isinstance(self.driver, AppiumDriver):
            DriverWrapper.__bases__ = MobileDriver,
            return MobileDriver
        if isinstance(self.driver, SeleniumDriver):
            DriverWrapper.__bases__ = WebDriver,
            return WebDriver
        else:
            raise DriverWrapperException('Cant specify Driver')
