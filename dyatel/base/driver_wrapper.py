from typing import Union

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.internal_utils import get_child_elements_with_names


class DriverWrapper(WebDriver, MobileDriver, PlayDriver):
    """ Driver object crossroad """

    __init_count = 0

    desktop = False
    selenium = False
    playwright = False

    mobile = False
    is_ios = False
    is_android = False
    is_xcui_driver = False
    is_safari_driver = False

    def __new__(cls, *args, **kwargs):
        if DriverWrapper.__init_count == 0:
            return super().__new__(cls)

        objects = {name: False for name in get_child_elements_with_names(cls, bool).keys()}
        return super().__new__(type("DifferentDriverWrapper", (DriverWrapper, ), objects))

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumDriver]):
        """
        Initializing of driver wrapper based on given driver source
        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.visual_regression_path = ''
        self.visual_reference_generation = False

        self.__set_base_class()
        super(self.__class__, self).__init__(driver=driver)

    def __repr__(self):
        cls = self.__class__
        class_name = cls.__name__
        base_class_name = cls.__base__.__name__
        mobile_data = f'mobile=(android={cls.is_android}, ios={cls.is_ios})' if cls.mobile else f'mobile={cls.mobile}'
        driver = self.instance if cls.playwright else self.driver
        return f'{class_name}(driver={driver}) at {hex(id(self))}, ' \
               f'base={base_class_name}, desktop={cls.desktop}, {mobile_data}'

    def __set_base_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class
        :return: driver wrapper class
        """
        DriverWrapper.__init_count += 1
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
