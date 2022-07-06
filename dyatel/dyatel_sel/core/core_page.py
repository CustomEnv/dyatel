from __future__ import annotations

from logging import info, debug
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from dyatel.base.element import Element
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.dyatel_sel.sel_utils import get_locator_type, get_legacy_selector
from dyatel.internal_utils import get_child_elements, WAIT_PAGE, Mixin


class CorePage(Mixin):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of core page with appium/selenium driver
        Contain same methods/data for both WebPage and MobilePage classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else self.locator

        self._element = None
        self.url = getattr(self, 'url', '')
        self.page_elements = get_child_elements(self, CoreElement)
        for el in self.page_elements:  # required for CoreElement
            if not getattr(el, '_initialized'):
                el.__init__(
                    locator=el.locator,
                    locator_type=el.locator_type,
                    name=el.name,
                    parent=el.parent,
                    wait=el.wait,
                )

    def reload_page(self, wait_page_load=True) -> CorePage:
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

    def open_page(self, url='') -> CorePage:
        """
        Open page with given url or use url from page class f url isn't given

        :param url: url for navigation
        :return: self
        """
        url = self.url if not url else url
        self.driver_wrapper.get(url)
        self.wait_page_loaded()
        return self

    def wait_page_loaded(self, silent=False, timeout=WAIT_PAGE) -> CorePage:
        """
        Wait until page loaded

        :param silent: erase log
        :param timeout: page/elements wait timeout
        :return: self
        """
        if not silent:
            info(f'Wait until page "{self.name}" loaded')

        wait = WebDriverWait(self.driver, timeout)
        wait.until(ec.visibility_of_element_located((self.locator_type, self.locator)))

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
        page_anchor = Element(locator=self.locator, locator_type=self.locator_type, name=self.name)

        if with_elements:
            for element in self.page_elements:
                if getattr(element, 'wait'):
                    result &= element.is_displayed(silent=True)
                    if not result:
                        debug(f'Element "{element.name}" is not displayed')

        result &= page_anchor.is_displayed()

        if self.url:
            result &= self.driver_wrapper.current_url == self.url

        return result

    @property
    def driver(self) -> Union[AppiumWebDriver, SeleniumWebDriver]:
        """
        Get source driver instance

        :return: SeleniumWebDriver for web test or AppiumWebDriver for mobile tests
        """
        return CoreDriver.driver

    @property
    def driver_wrapper(self) -> CoreDriver:
        """
        Get source driver wrapper instance

        :return: CoreDriver
        """
        return CoreDriver.driver_wrapper

    def set_driver(self, driver_wrapper: Union[WebDriver, MobileDriver]):
        """
        Set driver session

        :param driver_wrapper:
        :return:
        """
        CoreDriver.driver = driver_wrapper.driver
        CoreDriver.driver_wrapper = driver_wrapper
        return self
