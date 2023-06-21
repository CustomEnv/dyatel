from typing import Union

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException
from dyatel.js_scripts import get_inner_height_js, get_inner_width_js
from dyatel.utils.internal_utils import get_attributes_from_object, get_child_elements_with_names


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

    all_drivers = []

    def __new__(cls, *args, **kwargs):
        if DriverWrapper._init_count == 0:
            return super().__new__(cls)

        return super().__new__(type(f'ShadowDriverWrapper', (cls, ), get_attributes_from_object(cls)))  # noqa

    def __repr__(self):
        cls = self.__class__

        label = 'desktop'
        if cls.is_android:
            label = 'android'
        elif cls.is_ios:
            label = 'ios'

        driver = self.instance if cls.playwright else self.driver
        return f'{cls.__name__}({self.driver.label}={driver}) at {hex(id(self))}, platform={label}'  # noqa

    def __init__(self, driver: Union[PlaywrightDriver, AppiumDriver, SeleniumDriver]):
        """
        Initializing of driver wrapper based on given driver source

        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.all_drivers.append(driver)
        self.driver.label = f'{self.all_drivers.index(driver) + 1}_driver'
        self.__set_base_class()
        super(self.__class__, self).__init__(driver=self.driver)

    def quit(self, silent: bool = False):
        """
        Quit the driver instance

        :param: silent:
        :return: None
        """
        if not silent:
            self.log('Quit driver instance')

        super(self.__class__, self).quit()
        self.all_drivers.remove(self.driver)
        DriverWrapper._init_count -= 1

    def get_inner_window_size(self) -> dict:
        """
        Get inner size of driver window

        :return: {'height': value, 'width': value}
        """
        return {'height': self.execute_script(get_inner_height_js), 'width': self.execute_script(get_inner_width_js)}

    def __set_base_class(self):
        """
        Get driver wrapper class in according to given driver source, and set him as base class

        :return: driver wrapper class
        """
        self.__reset_settings()
        scls = self.__class__
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

        scls.__bases__ = bcls
        DriverWrapper._init_count += 1
        return self.__class__

    def __reset_settings(self):
        for name, _ in get_child_elements_with_names(self, bool).items():
            setattr(self.__class__, name, False)

