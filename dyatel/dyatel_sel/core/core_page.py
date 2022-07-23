from __future__ import annotations

from typing import List

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from dyatel.base.element import Element
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.sel_utils import get_locator_type, get_legacy_selector
from dyatel.internal_utils import (
    get_child_elements,
    Mixin,
    initialize_objects_with_args,
    DriverMixin,
)


class CorePage(Mixin, DriverMixin):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of core page with appium/selenium driver
        Contain same methods/data for both WebPage and MobilePage classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self._element = None
        self._driver_instance = CoreDriver

        if isinstance(self.driver, AppiumWebDriver):
            self.locator, self.locator_type = get_legacy_selector(locator, get_locator_type(locator))
        else:
            self.locator = locator
            self.locator_type = locator_type if locator_type else get_locator_type(locator)

        self.name = name if name else self.locator
        self.url = getattr(self, 'url', '')

        self.page_elements: List[CoreElement] = get_child_elements(self, CoreElement)
        initialize_objects_with_args(self.page_elements)

    @property
    def anchor(self) -> Element:
        """
        Get anchor Element of page

        :return: Element object
        """
        anchor = Element(locator=self.locator, locator_type=self.locator_type, name=self.name)
        anchor._driver_instance = self.driver_wrapper
        return anchor
