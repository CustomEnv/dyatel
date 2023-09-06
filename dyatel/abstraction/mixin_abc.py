from abc import ABC
from typing import Union

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from playwright.sync_api import Page as PlaywrightSourcePage
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.base.driver_wrapper import DriverWrapper


class MixinABC(ABC):

    @property
    def driver(self) -> Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightSourcePage]:
        """
        Get source driver instance

        :return: SeleniumWebDriver/AppiumWebDriver/PlaywrightWebDriver
        """
        raise NotImplementedError()

    @property
    def driver_wrapper(self) -> DriverWrapper:
        """
        Get source driver wrapper instance

        :return: driver_wrapper
        """
        raise NotImplementedError()

    @driver_wrapper.setter
    def driver_wrapper(self, driver_wrapper: DriverWrapper):
        """
        Set source driver wrapper instance
        """
        raise NotImplementedError()

    def log(self, message: str, level: str = 'info') -> None:
        """
        Log message in format:
          ~ [time][level][driver_index][module][function:line] <message>
          ~ [Aug 14][16:04:22.767][I][2_driver][play_element.py][is_displayed:328] Check visibility of "Mouse page"

        :param message: info message
        :param level: log level
        :return: None
        """
        raise NotImplementedError()
