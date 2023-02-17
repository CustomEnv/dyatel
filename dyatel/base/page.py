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
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.internal_utils import WAIT_PAGE
from dyatel.mixins.element_mixin import shadow_class, repr_builder, set_base_class, all_mid_level_elements
from dyatel.mixins.previous_object_mixin import PreviousObjectDriver


class Page(WebPage, MobilePage, PlayPage):
    """ Page object crossroad. Should be defined as class """

    def __new__(cls, *args, **kwargs):
        return shadow_class(cls, Page)

    def __repr__(self):
        return repr_builder(self, Page)

    def __init__(  # noqa
            self,
            locator: str = '',
            locator_type: str = '',
            name: str = '',
            driver_wrapper: Union[DriverWrapper, Any] = None,
            **kwargs
    ):
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
        self._is_page = True

        self._driver_instance = get_driver_wrapper_from_object(driver_wrapper)
        self.element_class = self.__set_base_class()
        super(self.element_class, self).__init__(
            locator=self.locator,
            locator_type=self.locator_type,
            name=self.name
        )
        # it's necessary to leave it after init
        if driver_wrapper:
            self._set_driver(self._driver_instance, all_mid_level_elements())
        elif self.driver_wrapper:
            PreviousObjectDriver().set_driver_from_previous_object_for_page_or_group(self, 5)

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

        self.anchor.wait_element(timeout=timeout, silent=True)

        for element in self.page_elements:
            if getattr(element, 'wait') is False:
                element.wait_element_hidden(timeout=timeout, silent=True)
            elif getattr(element, 'wait') is True:
                element.wait_element(timeout=timeout, silent=True)
        return self

    def is_page_opened(self, with_elements: bool = False, with_url: bool = False) -> bool:
        """
        Check is current page opened or not

        :param with_elements: is page opened with signed elements
        :param with_url: is page opened check with url
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

        if self.url and with_url:
            result &= self.driver_wrapper.current_url == self.url

        return result

    @property
    def anchor(self) -> Element:
        """
        Get anchor element of the page

        :return: Element object
        """
        anchor = Element(locator=self.locator, locator_type='', name=self.name)
        anchor._driver_instance = self.driver_wrapper
        return anchor

    def __set_base_class(self) -> Page:
        """
        Get page class in according to current driver, and set him as base class

        :return: page class
        """
        if isinstance(self.driver, PlaywrightDriver):
            cls = PlayPage,
        elif isinstance(self.driver, AppiumDriver):
            cls = MobilePage,
        elif isinstance(self.driver, SeleniumDriver):
            cls = WebPage,
        else:
            raise DriverWrapperException(f'Cant specify {Page.__name__}')

        return set_base_class(self, Page, cls)
