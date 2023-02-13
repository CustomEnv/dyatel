from __future__ import annotations

from typing import List

from dyatel.base.element import Element
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.sel_utils import get_locator_type
from dyatel.mixins.internal_utils import get_child_elements, initialize_objects_with_args
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.log_mixin import LogMixin


class CorePage(DriverMixin, LogMixin):

    def __init__(self, locator: str, locator_type: str, name: str):
        """
        Initializing of core page with appium/selenium driver
        Contain same methods/data for both WebPage and MobilePage classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self._element = None

        self.locator = locator
        self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.name = name if name else locator

        self.name = name if name else self.locator
        self.url = getattr(self, 'url', '')

        self.page_elements: List[CoreElement] = get_child_elements(self, CoreElement)
        initialize_objects_with_args(self.page_elements)
