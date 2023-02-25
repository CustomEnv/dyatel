from typing import Union

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException
from dyatel.js_scripts import get_inner_height_js, get_inner_width_js
from dyatel.mixins.core_mixin import (
    get_child_elements_with_names,
    driver_with_index,
    get_all_attributes_from_object,
)


class DriverWrapper(WebDriver, MobileDriver, PlayDriver):
    """ Driver object crossroad """

    _init_count = 0

    desktop = False
    selenium = False
    playwright = False

    mobile = False
    is_ios = False
    is_android = False
    is_simulator = False
    is_real_device = False
    is_multiplatform = False

    def __new__(cls, *args, **kwargs):
        if DriverWrapper._init_count == 0:
            return super().__new__(cls)

        class_objects = get_all_attributes_from_object(cls, stop_on_base=True)
        return super().__new__(type(f'Shadow{DriverWrapper.__name__}', (cls, ), class_objects))  # noqa

    def __repr__(self):
        cls = self.__class__

        label = 'desktop'
        if cls.is_android:
            label = 'android'
        elif cls.is_ios:
            label = 'ios'

        driver = self.instance if cls.playwright else self.driver
        index = driver_with_index(self.driver_wrapper, driver)
        return f'{cls.__name__}({index}={driver}) at {hex(id(self))}, platform={label}'

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumDriver]):
        """
        Initializing of driver wrapper based on given driver source

        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.__set_base_class()
        super(self.__class__, self).__init__(driver=self.driver)

    def get_inner_window_size(self) -> dict:
        """
        Get inner size of driver window

        :return: {'height': value, 'width': value}
        """
        return {'height': self.execute_script(get_inner_height_js), 'width': self.execute_script(get_inner_width_js)}

    def quit(self, silent=False):
        super(self.__class__, self).quit(silent=silent)
        DriverWrapper.all_drivers.remove(self.driver)
        DriverWrapper._init_count -= 1

        if self.driver == DriverWrapper.driver:  # Clear only if original driver closed
            DriverWrapper.driver = None
            DriverWrapper.instance = None
            DriverWrapper.driver_wrapper = None

    def __set_base_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class

        :return: driver wrapper class
        """
        self.__reset_settings()
        dcls, scls = DriverWrapper, self.__class__
        scls.all_drivers = dcls.all_drivers
        if isinstance(self.driver, PlaywrightDriver):
            scls.playwright = True
            scls.desktop = True
            bcls = PlayDriver,
        elif isinstance(self.driver, AppiumDriver):
            scls.mobile = True
            bcls = MobileDriver,
        elif isinstance(self.driver, SeleniumDriver):
            scls.desktop = True
            scls.selenium = True
            bcls = WebDriver,
        else:
            raise DriverWrapperException('Cant specify Driver')

        self.__set_multiplatform(dcls, scls)
        scls.__bases__ = bcls
        dcls._init_count += 1
        return self.__class__

    def __reset_settings(self):
        for name, _ in get_child_elements_with_names(self, bool).items():
            setattr(self.__class__, name, False)

    def __set_multiplatform(self, dcls, scls):
        if (dcls.mobile and scls.desktop) or (dcls.desktop and scls.mobile):
            dcls.is_multiplatform = True
            scls.is_multiplatform = True
