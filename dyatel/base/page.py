from __future__ import annotations

from logging import debug, info

from dyatel.base.driver import Driver
from dyatel.base.element import Element
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from dyatel.internal_utils import WAIT_PAGE


class Page(WebPage, MobilePage, PlayPage):
    """ Page object crossroad. Should be defined as class """

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of page based on current driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self._driver_instance = Driver
        self.__set_page_class()
        super().__init__(locator=locator, locator_type=locator_type, name=name)

    def reload_page(self, wait_page_load=True) -> Page:
        """
        Reload current page

        :param wait_page_load: wait until anchor will be element loaded
        :return: self
        """
        info(f'Reload {self.name} page')
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
            info(f'Wait until page "{self.name}" loaded')

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
                        debug(f'Element "{element.name}" is not displayed')

        result &= self.anchor.is_displayed()

        if self.url:
            result &= self.driver_wrapper.current_url == self.url

        return result

    def set_driver(self, driver_wrapper) -> Page:
        """
        Set driver instance for page and elements/groups

        :param driver_wrapper: driver wrapper object ~ Driver/WebDriver/MobileDriver/CoreDriver/PlayDriver
        :return: self
        """
        self._set_driver(driver_wrapper, Element)
        return self

    def __set_page_class(self):
        """
        Get page class in according to current driver, and set him as base class

        :return: page class
        """
        if PlayDriver.driver:
            Page.__bases__ = PlayPage,
            return PlayPage
        elif CoreDriver.driver and CoreDriver.mobile:
            Page.__bases__ = MobilePage,
            return MobilePage
        elif CoreDriver.driver and not CoreDriver.mobile:
            Page.__bases__ = WebPage,
            return WebPage
        else:
            raise Exception('Cant specify Page')
