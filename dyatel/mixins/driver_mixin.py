from __future__ import annotations

from copy import copy
from typing import Union, Any

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from playwright.sync_api import Page as PlaywrightWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver


def get_driver_wrapper_from_object(obj: Union[DriverWrapper, Any]):
    """
    Get driver wrapper from custom object

    :param obj: custom object. Can be driver_wrapper or object with driver_wrapper
    :return: driver wrapper object
    """
    if obj is None:
        return DriverWrapper

    if isinstance(obj, (DriverWrapper, PlayDriver, WebDriver, MobileDriver)):
        driver_wrapper_instance = obj
    elif hasattr(obj, 'driver_wrapper'):
        driver_wrapper_instance = obj.driver_wrapper
    else:
        obj_nfo = f'"{getattr(obj, "name")}" of "{obj.__class__}"' if obj else obj
        raise Exception(f'Cant get driver_wrapper from {obj_nfo}')

    return driver_wrapper_instance


class DriverMixin:

    @property
    def driver(self) -> Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightWebDriver]:
        """
        Get source driver instance

        :return: SeleniumWebDriver/AppiumWebDriver/PlaywrightWebDriver
        """
        driver_instance = getattr(self, '_driver_instance', DriverWrapper)
        return driver_instance.driver

    @driver.setter
    def driver(self, driver: Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightWebDriver]):
        """ Set source driver instance """
        setattr(self, '_driver_instance', driver)

    @property
    def driver_wrapper(self) -> Union[WebDriver, MobileDriver, PlayDriver, DriverWrapper]:
        """
        Get source driver wrapper instance

        :return: driver_wrapper
        """
        driver_instance = getattr(self, '_driver_instance', DriverWrapper)
        return driver_instance.driver_wrapper

    @driver_wrapper.setter
    def driver_wrapper(self, driver_wrapper: Union[WebDriver, MobileDriver, PlayDriver, DriverWrapper]):
        """ Set source driver wrapper instance """
        setattr(self, '_driver_instance', driver_wrapper)
