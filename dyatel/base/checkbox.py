from __future__ import annotations

from typing import Any

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_checkbox import PlayCheckbox
from dyatel.dyatel_sel.core.core_checkbox import CoreCheckbox as SelCheckbox
from dyatel.mixins.internal_utils import get_platform_locator, driver_index
from dyatel.mixins.previous_object_mixin import PreviousObjectDriver


class Checkbox(SelCheckbox, PlayCheckbox):
    """ Checkbox object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str = '', locator_type: str = '', name: str = '',
                 parent: Any = None, wait: bool = False, **kwargs):
        """
        Initializing of checkbox based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of checkbox. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of checkbox (will be attached to logs)
        :param parent: parent of checkbox. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait

        self._driver_instance = DriverWrapper
        self._initialized = False
        self._init_locals = locals()

        self.element_class = self.__set_base_class()
        if self.element_class:
            self._initialized = True
            super().__init__(locator=self.locator, locator_type=self.locator_type, name=self.name, parent=self.parent,
                             wait=self.wait)

    def __repr__(self):
        cls = self.__class__
        class_name = cls.__name__
        locator = f'locator="{get_platform_locator(self)}"'
        index = driver_index(self.driver_wrapper, self.driver)
        driver = index if index else 'driver'
        parent = self.parent.__class__.__name__ if self.parent else None
        return f'{class_name}({locator}, locator_type="{self.locator_type}", name="{self.name}", parent={parent}) '\
               f'at {hex(id(self))}, {driver}={self.driver}'

    def __set_base_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        if self.driver_wrapper:
            PreviousObjectDriver().set_driver_from_previous_object_for_element(self, 5)

            if not getattr(self, '_initialized', False):
                if self.parent is None:
                    PreviousObjectDriver().set_parent_from_previous_object_for_element(self, 5)

        if isinstance(self.driver, PlaywrightDriver):
            Checkbox.__bases__ = PlayCheckbox,
            return PlayCheckbox
        elif isinstance(self.driver, (SeleniumDriver, AppiumDriver)):
            Checkbox.__bases__ = SelCheckbox,
            return SelCheckbox

        # No exception due to delayed initialization
