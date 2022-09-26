from __future__ import annotations

from typing import Any

from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_checkbox import PlayCheckbox
from dyatel.dyatel_sel.core.core_checkbox import CoreCheckbox as SelCheckbox
from dyatel.mixins.internal_utils import get_frame


class Checkbox(SelCheckbox, PlayCheckbox):
    """ Checkbox object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str, locator_type: str = '', name: str = '',
                 parent: Any = None, wait: bool = False):
        """
        Initializing of checkbox based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of checkbox. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of checkbox (will be attached to logs)
        :param parent: parent of checkbox. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait

        self._driver_instance = DriverWrapper
        self._initialized = False

        self.element_class = self.__set_base_class()
        if self.element_class:
            super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    def __set_base_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        if self.driver_wrapper:
            if len(self.driver_wrapper.all_drivers) > 1:
                if self.driver:
                    from dyatel.base.group import Group
                    if not isinstance(self, Group):
                        frame = get_frame(3)
                        prev_object = frame.f_locals.get('self', None)
                        if prev_object:
                            self.driver_wrapper = prev_object.driver_wrapper

        if isinstance(self.driver, PlaywrightDriver):
            Checkbox.__bases__ = PlayCheckbox,
            return PlayCheckbox
        elif isinstance(self.driver, (SeleniumDriver, AppiumDriver)):
            Checkbox.__bases__ = SelCheckbox,
            return SelCheckbox

        # No exception due to delayed initialization
