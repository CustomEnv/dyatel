from __future__ import annotations

from typing import Union, Any

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from playwright.sync_api import Page as PlaywrightSourcePage
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.base.driver_wrapper import DriverWrapper, DriverWrapperSessions


def get_driver_wrapper_from_object(obj: Union[DriverWrapper, Any]):
    """
    Get driver wrapper from custom object

    :param obj: custom object. Can be driver_wrapper or object with driver_wrapper
    :return: driver wrapper object
    """
    if obj is None:
        return DriverWrapperSessions.first_session()

    if isinstance(obj, DriverWrapper):
        driver_wrapper_instance = obj
    elif hasattr(obj, 'driver_wrapper'):
        driver_wrapper_instance = obj.driver_wrapper
    else:
        obj_nfo = f'"{getattr(obj, "name")}" of "{obj.__class__}"' if obj else obj
        raise Exception(f'Cant get driver_wrapper from {obj_nfo}')

    return driver_wrapper_instance


class DriverMixin:

    _driver_wrapper = None

    @property
    def driver(self) -> Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightSourcePage]:
        """
        Get source driver instance

        :return: SeleniumWebDriver/AppiumWebDriver/PlaywrightSourcePage
        """
        return getattr(self.driver_wrapper, 'driver', None)

    @property
    def driver_wrapper(self) -> DriverWrapper:
        """
        Get source driver wrapper instance

        :return: driver_wrapper
        """
        return self._driver_wrapper

    @driver_wrapper.setter
    def driver_wrapper(self, driver_wrapper: DriverWrapper):
        """ Set source driver wrapper instance """
        self._driver_wrapper = driver_wrapper
