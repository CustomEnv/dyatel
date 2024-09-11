from __future__ import annotations

from typing import Union, Any, List, Type

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.abstraction.page_abc import PageABC
from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object, DriverMixin
from dyatel.mixins.internal_mixin import InternalMixin
from dyatel.mixins.objects.locator import Locator
from dyatel.utils.logs import Logging
from dyatel.utils.previous_object_driver import PreviousObjectDriver, set_instance_frame
from dyatel.utils.internal_utils import (
    WAIT_PAGE,
    initialize_objects,
    get_child_elements_with_names,
    get_child_elements,
    is_element_instance,
)


class Page(DriverMixin, InternalMixin, Logging, PageABC):
    """ Page object crossroad. Should be defined as class """

    _object = 'page'
    _base_cls: Type[PlayPage, MobilePage, WebPage]

    def __new__(cls, *args, **kwargs):
        instance = super(Page, cls).__new__(cls)
        set_instance_frame(instance)
        return instance

    def __repr__(self):
        return self._repr_builder()

    def __call__(self, *arg, **kwargs):
        return self

    def __init__(
            self,
            locator: Union[Locator, str] = '',
            name: str = '',
            driver_wrapper: Union[DriverWrapper, Any] = None,
            **kwargs
    ):
        """
        Initializing of page based on current driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param name: name of page (will be attached to logs)
        :param driver_wrapper: set custom driver for page and page elements
        """
        self._validate_inheritance()
        self._check_kwargs(kwargs)

        self.driver_wrapper = get_driver_wrapper_from_object(driver_wrapper)
        
        self.anchor = Element(locator, name=name, driver_wrapper=self.driver_wrapper)
        self.locator = self.anchor.locator
        self.locator_type = self.anchor.locator_type
        self.name = self.anchor.name

        self.url = getattr(self, 'url', '')

        self._init_locals = locals()
        self._modify_page_driver_wrapper(driver_wrapper)
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
            self._base_cls = PlayPage
        elif isinstance(self.driver, AppiumDriver):
            self._base_cls = MobilePage
        elif isinstance(self.driver, SeleniumDriver):
            self._base_cls = WebPage
        else:
            raise DriverWrapperException(f'Cant specify {Page.__name__}')

        self._set_static(self._base_cls)
        self._base_cls.__init__(self)

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

        self.anchor.wait_visibility(timeout=timeout, silent=True)

        for element in self.page_elements:
            if getattr(element, 'wait') is False:
                element.wait_hidden(timeout=timeout, silent=True)
            elif getattr(element, 'wait') is True:
                element.wait_visibility(timeout=timeout, silent=True)
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

    def _modify_children(self):
        """
        Initializing of attributes with type == Element.
        Required for classes with base == Page.
        """
        initialize_objects(self, get_child_elements_with_names(self, Element), Element)

    def _modify_page_driver_wrapper(self, driver_wrapper: Any):
        """
        Modify current object if driver_wrapper is not given. Required for Page that placed into functions:
        - sets driver from previous object
        """
        if not driver_wrapper:
            PreviousObjectDriver().set_driver_from_previous_object(self)

    def _validate_inheritance(self):
        cls = self.__class__
        mro = cls.__mro__

        for item in mro:
            if is_element_instance(item):
                raise TypeError(
                    f"You cannot make an inheritance for {cls.__name__} from both Page and Group/Element objects")
