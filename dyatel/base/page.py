from __future__ import annotations

from typing import Union, Any

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object, PreviousObjectDriver
from dyatel.mixins.internal_utils import WAIT_PAGE, get_platform_locator, driver_index


class Page(WebPage, MobilePage, PlayPage):
    """ Page object crossroad. Should be defined as class """

    def __init__(self, locator: str, locator_type: str = '', name: str = '',
                 driver_wrapper: Union[DriverWrapper, Any] = None, **kwargs):
        """
        Initializing of page based on current driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of page (will be attached to logs)
        :param driver_wrapper: set custom driver for page and page elements
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self._init_locals = locals()

        self._driver_instance = DriverWrapper
        self.__set_base_class()
        super().__init__(locator=self.locator, locator_type=self.locator_type, name=self.name)
        # it's necessary to leave it after init
        if driver_wrapper:
            self._driver_instance = get_driver_wrapper_from_object(self, driver_wrapper)
            self.set_driver(self._driver_instance)
        elif len(self.driver_wrapper.all_drivers) > 1:
            PreviousObjectDriver().set_driver_from_previous_object_for_page(self, 5)

    def __repr__(self):
        cls = self.__class__
        class_name = cls.__name__
        base_class_name = cls.__base__.__base__.__name__
        locator = f'locator="{get_platform_locator(self)}"'
        index = driver_index(self.driver_wrapper, self.driver)
        driver = index if index else 'driver'
        return f'{class_name}({locator}, locator_type="{self.locator_type}", name="{self.name}") at {hex(id(self))}'\
               f', base={base_class_name}, {driver}={self.driver}'

    # Following methods works same for both Selenium/Appium and Playwright APIs using dyatel methods

    def reload_page(self, wait_page_load=True) -> Page:
        """
        Reload current page

        :param wait_page_load: wait until anchor will be element loaded
        :return: self
        """
        self.log(f'Reload "{self.name}" page')
        self.driver_wrapper.refresh()

        if wait_page_load:
            self.wait_page_loaded()

        return self

    def open_page(self, url='') -> Page:
        """
        Open page with given url or use url from page class f url isn't given

        :param url: url for navigation
        :return: self
        """
        url = self.url if not url else url
        self.driver_wrapper.get(url)
        self.wait_page_loaded()
        return self

    def wait_page_loaded(self, silent=False, timeout=WAIT_PAGE) -> Page:
        """
        Wait until page loaded

        :param silent: erase log
        :param timeout: page/elements wait timeout
        :return: self
        """
        if not silent:
            self.log(f'Wait until page "{self.name}" loaded')

        self.anchor.wait_element(timeout=timeout)

        for element in self.page_elements:
            if getattr(element, 'wait'):
                element.wait_element(timeout=timeout, silent=True)
        return self

    def is_page_opened(self, with_elements=False) -> bool:
        """
        Check is current page opened or not

        :param with_elements: is page opened with signed elements
        :return: self
        """
        result = True

        if with_elements:
            for element in self.page_elements:
                if getattr(element, 'wait'):
                    result &= element.is_displayed(silent=True)
                    if not result:
                        self.log(f'Element "{element.name}" is not displayed', level='debug')

        result &= self.anchor.is_displayed()

        if self.url:
            result &= self.driver_wrapper.current_url == self.url

        return result

    def set_driver(self, driver_wrapper: DriverWrapper) -> Page:
        """
        Set driver instance for page and elements/groups

        :param driver_wrapper: driver wrapper object ~ DriverWrapper/WebDriver/MobileDriver/CoreDriver/PlayDriver
        :return: self
        """
        if not driver_wrapper:
            return self

        self._set_driver(driver_wrapper, Element)
        return self

    def __set_base_class(self):
        """
        Get page class in according to current driver, and set him as base class

        :return: page class
        """
        if isinstance(self.driver, PlaywrightDriver):
            Page.__bases__ = PlayPage,
            return PlayPage
        elif isinstance(self.driver, AppiumDriver):
            Page.__bases__ = MobilePage,
            return MobilePage
        elif isinstance(self.driver, SeleniumDriver):
            Page.__bases__ = WebPage,
            return WebPage
        else:
            raise DriverWrapperException('Cant specify Page')
