from typing import Union, Callable

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException
from dyatel.js_scripts import get_inner_height_js, get_inner_width_js
from dyatel.mixins.internal_utils import get_child_elements_with_names, driver_index


class DriverWrapper(WebDriver, MobileDriver, PlayDriver):
    """ Driver object crossroad """

    _init_count = 0

    desktop = False
    selenium = False
    playwright = False

    mobile = False
    is_ios = False
    is_android = False
    is_xcui_driver = False
    is_safari_driver = False

    def __new__(cls, *args, **kwargs):
        if DriverWrapper._init_count == 0:
            return super().__new__(cls)

        class_objects = {}
        for name, value in get_child_elements_with_names(cls, Callable).items():
            if not name.endswith('__'):
                class_objects.update({name: value})
        class_objects.update({name: False for name in get_child_elements_with_names(cls, bool).keys()})
        class_objects.update({'__repr__': cls.__repr__})
        return super().__new__(type("DifferentDriverWrapper", (DriverWrapper, ), class_objects))

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumDriver]):
        """
        Initializing of driver wrapper based on given driver source
        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver

        self.__set_base_class()
        super(self.__class__, self).__init__(driver=self.driver)

    def __repr__(self):
        cls = self.__class__
        class_name = cls.__name__
        base_class_name = cls.__base__.__name__
        mobile_data = f'mobile=(android={cls.is_android}, ios={cls.is_ios})' if cls.mobile else f'mobile={cls.mobile}'
        driver = self.instance if cls.playwright else self.driver
        index = driver_index(self.driver_wrapper, self.driver)
        driver_with_index = index if index else 'driver'
        return f'{class_name}({driver_with_index}={driver}) at {hex(id(self))}, ' \
               f'base={base_class_name}, desktop={cls.desktop}, {mobile_data}'

    def get_inner_window_size(self) -> dict:
        """
        Get inner size of driver window

        :return: {'height': value, 'width': value}
        """
        return {'height': self.execute_script(get_inner_height_js), 'width': self.execute_script(get_inner_width_js)}

    def __getattribute__(self, item):
        if item == 'quit':
            DriverWrapper._init_count = 0
        return super().__getattribute__(item)

    def __set_base_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class
        :return: driver wrapper class
        """
        DriverWrapper._init_count += 1
        if isinstance(self.driver, PlaywrightDriver):
            self.__class__.__bases__ = PlayDriver,
            self.__class__.mobile = False
            self.__class__.playwright = True
            self.__class__.desktop = True
            return PlayDriver
        if isinstance(self.driver, AppiumDriver):
            self.__class__.__bases__ = MobileDriver,
            self.__class__.mobile = True
            self.__class__.desktop = False
            return MobileDriver
        if isinstance(self.driver, SeleniumDriver):
            self.__class__.__bases__ = WebDriver,
            self.__class__.mobile = False
            self.__class__.desktop = True
            self.__class__.selenium = True
            return WebDriver
        else:
            raise DriverWrapperException('Cant specify Driver')
