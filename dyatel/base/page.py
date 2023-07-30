from __future__ import annotations

from typing import Union, Any, List, Type

from playwright.sync_api import Browser as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.abstraction.page_abs import PageAbstraction
from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object, DriverMixin
from dyatel.mixins.internal_mixin import InternalMixin
from dyatel.utils.logs import Logging
from dyatel.utils.previous_object_driver import PreviousObjectDriver
from dyatel.utils.internal_utils import (
    WAIT_PAGE,
    initialize_objects,
    get_child_elements_with_names,
    get_child_elements,
)


class Page(DriverMixin, InternalMixin, Logging, PageAbstraction):
    """ Page object crossroad. Should be defined as class """

    _object = 'page'

    def __repr__(self):
        return self._repr_builder()

    def __call__(self, *arg, **kwargs):
        return self

    def __init__(
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
        self._validate_inheritance()
        self._check_kwargs(kwargs)

        self.locator = locator
        self.locator_type = locator_type
        self.name = name if name else locator

        self.url = getattr(self, 'url', '')

        self._element = None
        self._init_locals = locals()
        self._driver_instance = get_driver_wrapper_from_object(driver_wrapper)
        self._modify_object()
        self._modify_children()
        self._safe_setter('__base_obj_id', id(self))

        self.page_elements: List[Element] = get_child_elements(self, Element)

        self.__init_base_class__()

    def __init_base_class__(self) -> None:
        """
        Initialise base class according to current driver, and set his methods

        :return: None
        """
        if isinstance(self.driver, PlaywrightDriver):
            cls = PlayPage
        elif isinstance(self.driver, AppiumDriver):
            cls = MobilePage
        elif isinstance(self.driver, SeleniumDriver):
            cls = WebPage
        else:
            raise DriverWrapperException(f'Cant specify {Page.__name__}')

        self._set_static(cls)
        cls.__init__(self)

    # Following methods works same for both Selenium/Appium and Playwright APIs using internal methods

    def reload_page(self, wait_page_load: bool = True) -> Page:
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

    def open_page(self, url: str = '') -> Page:
        """
        Open page with given url or use url from page class f url isn't given

        :param url: url for navigation
        :return: self
        """
        url = self.url if not url else url
        self.driver_wrapper.get(url)
        self.wait_page_loaded()
        return self

    def wait_page_loaded(self, silent: bool = False, timeout: Union[int, float] = WAIT_PAGE) -> Page:
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
        anchor = Element(locator=self.locator, locator_type=self.locator_type, name=self.name)
        return anchor

    def _modify_children(self):
        """
        Initializing of attributes with type == Element.
        Required for classes with base == Page.
        """
        initialize_objects(self, get_child_elements_with_names(self, Element), Element)

    def _modify_object(self):
        """
        Modify current object. Required for Page that placed into functions:
        - set driver from previous object if previous driver different.
        """
        PreviousObjectDriver().set_driver_from_previous_object_for_page_or_group(self, 5)

    def _validate_inheritance(self):
        cls = self.__class__
        mro = cls.__mro__

        if Element in mro or Group in mro:
            raise TypeError(
                f"You cannot make an inheritance for {cls.__name__} from both Page and Group/Element objects")
