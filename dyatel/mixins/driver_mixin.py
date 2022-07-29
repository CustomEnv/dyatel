from __future__ import annotations

from copy import copy
from typing import Union

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from playwright.sync_api import Browser as PlaywrightWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.base.driver import Driver
from dyatel.mixins.internal_utils import get_child_elements, get_child_elements_with_names


class DriverMixin:

    @property
    def driver(self) -> Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightWebDriver]:
        """
        Get source driver instance

        :return: SeleniumWebDriver/AppiumWebDriver/PlaywrightWebDriver
        """
        return self._driver_instance.driver

    @property
    def driver_wrapper(self) -> Driver:
        """
        Get source driver wrapper instance

        :return: driver_wrapper
        """
        return self._driver_instance.driver_wrapper

    def _set_driver(self, driver_wrapper, instance_class):
        """

        :param driver_wrapper:
        :param instance_class:
        :return:
        """
        new_driver = copy(self.driver_wrapper)
        setattr(new_driver, 'driver', copy(self.driver_wrapper.driver))
        setattr(new_driver, 'driver_wrapper', copy(self.driver_wrapper))

        new_driver.driver = driver_wrapper.driver
        new_driver.driver_wrapper = driver_wrapper

        self._driver_instance = new_driver
        self.__set_driver_for_attr(instance_class, self, new_driver)
        self.page_elements = get_child_elements(self, instance_class)

    def __set_driver_for_attr(self, instance_class, base_obj, driver_wrapper):
        """

        :param instance_class:
        :param base_obj:
        :param driver_wrapper:
        :return:
        """
        child_elements = get_child_elements_with_names(base_obj, instance_class).items()

        for name, child in child_elements:
            wrapped_child = copy(child)
            wrapped_child._driver_instance = driver_wrapper
            setattr(base_obj, name, wrapped_child)
            self.__set_driver_for_attr(instance_class, wrapped_child, driver_wrapper)

        return self
