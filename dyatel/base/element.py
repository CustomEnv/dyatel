from __future__ import annotations

import time
from logging import info
from typing import Any

from dyatel.base.driver import Driver
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.internal_utils import WAIT_EL


class Element(WebElement, MobileElement, PlayElement):
    """ Element object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str, locator_type='', name='', parent: Any = None, wait=False):
        """
        Initializing of element based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of element. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait
        self._initialized = False
        self._driver_instance = Driver

        self.element_class = self.__get_element_class()
        if self.element_class:
            super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    def __get_element_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        if PlayDriver.driver:
            Element.__bases__ = PlayElement,
            return PlayElement
        elif CoreDriver.driver and CoreDriver.mobile:
            Element.__bases__ = MobileElement,
            return MobileElement
        elif CoreDriver.driver and not CoreDriver.mobile:
            Element.__bases__ = WebElement,
            return WebElement

    # Following methods works same for both Selenium/Appium and Playwright APIs

    # Elements interaction

    def set_text(self, text, silent=False) -> Element:
        """
        Set (clear and type) text in current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Set text in "{self.name}"')

        self.clear_text(silent=True).type_text(text, silent=True)
        return self

    # Elements waits

    def wait_elements_count(self, elements_count, timeout=WAIT_EL, silent=False) -> Element:
        """
        Wait until elements count will be equal to expected value

        :param: elements_count: expected elements count
        :param: timeout: wait timeout
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until elements count will be equal to "{elements_count}"')

        start_time = time.time()
        while time.time() - start_time < timeout and self.get_elements_count() != elements_count:
            pass

        actual_elements_count = self.get_elements_count()

        if actual_elements_count != elements_count:
            raise Exception(f'Unexpected elements count of "{self.name}". '
                            f'Actual: {actual_elements_count}; Expected: {elements_count}')

        return self

    def wait_element_text(self, timeout=WAIT_EL, silent=False):
        """
        Wait non empty text in element

        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait for any text is available in "{self.name}"')

        start_time = time.time()
        while time.time() - start_time < timeout and not self.get_text:
            pass

        if not self.get_text:
            raise Exception(f'Text of "{self.name}" is empty')

        return self

    def wait_element_value(self, timeout=WAIT_EL, silent=False):
        """
        Wait non empty value in element

        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait for any value is available in "{self.name}"')

        start_time = time.time()
        while time.time() - start_time < timeout and not self.get_value:
            pass

        if not self.get_value:
            raise Exception(f'Value of "{self.name}" is empty')

        return self
