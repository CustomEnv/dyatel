from __future__ import annotations

from dyatel.base.element import Element
from dyatel.mixins.internal_utils import WAIT_EL


class CoreCheckbox(Element):

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False):
        """
        Initializing of core checkbox with appium/selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects etc.
        :param wait: add element waiting in `wait_page_loaded` function of CorePage
        """
        super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    def wait_element(self, timeout: int = WAIT_EL, silent: bool = False):
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        self.wait_availability(silent=True)
        return self

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: bool
        """
        return self.element.is_selected()

    def check(self) -> CoreCheckbox:
        """
        Check current checkbox

        :return: self
        """
        self.element = self._get_element()

        try:
            if not self.is_checked():
                self.click()
        finally:
            self.element = None

        return self

    def uncheck(self) -> CoreCheckbox:
        """
        Uncheck current checkbox

        :return: self
        """
        self.element = self._get_element()

        try:
            if self.is_checked():
                self.click()
        finally:
            self.element = None

        return self

    @property
    def text(self) -> str:
        """
        Get text of current checkbox

        :return: checkbox text
        """
        element = self.element
        return element.text if element.text else element.get_attribute('value')
