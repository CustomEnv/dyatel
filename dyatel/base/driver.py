from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver


class Driver(WebDriver, MobileDriver, PlayDriver):

    def __init__(self, driver):
        self.driver = driver
        self.driver_class = self.__get_driver_class()
        self.driver_class.__init__(self, driver)

    def __get_driver_class(self):
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
