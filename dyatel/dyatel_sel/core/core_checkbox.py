from __future__ import annotations

import time
from logging import info

from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.internal_utils import WAIT_EL


class CoreCheckbox(CoreElement):

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False, by_attr=False):
        """
        Initializing of core checkbox with appium/selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects etc.
        :param wait: add element waiting in `wait_page_loaded` function of CorePage
        :param by_attr: get is_checked state by custom attribute
        """
        super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)
        self.checked = None
        self.by_attr = by_attr

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium WebElement object

        :return: selenium WebElement
        """
        self.wait_availability()
        return self._get_element(wait=False)

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: bool
        """
        is_checked_selenium = self.element.is_selected()
        return self.checked if self.by_attr else is_checked_selenium

    def check(self) -> CoreCheckbox:
        """
        Check current checkbox

        :return: self
        """
        if not self.is_checked():
            self.wait_clickable(silent=True).element.click()
            self.checked = True

        return self

    def uncheck(self) -> CoreCheckbox:
        """
        Uncheck current checkbox

        :return: self
        """
        if self.is_checked():
            self.wait_clickable(silent=True).element.click()
            self.checked = False

        return self

    @property
    def get_text(self) -> str:
        """
        Get text of current checkbox

        :return: checkbox text
        """
        return self.element.text if self.element.text else self.element.get_attribute('value')

    def wait_clickable(self, silent=False, timeout=WAIT_EL) -> CoreCheckbox:
        """
        Wait until checkbox become clickable
        Selenium `element_to_be_clickable` doesn't work for some checkboxes

        :param silent: erase log
        :param timeout: wait timeout
        :return: self
        """
        if not silent:
            info(f'Wait until "{self.name}" become clickable')

        start_time = time.time()
        while time.time() - start_time < timeout and not self.element.is_enabled():
            pass

        if not self.element.is_enabled():
            raise Exception(f'"{self.name}" not clickable')

        return self

    def wait_availability(self, timeout=WAIT_EL, silent=False) -> CoreElement:
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            info(f'Wait until presence of "{self.name}"')

        start_time = time.time()

        while time.time() - start_time < timeout and not self.is_available():
            pass

        if not self.is_available():
            raise Exception(f'Can\'t wait element in DOM "{self.name}". {self.get_element_logging_data()}')

        return self
