from __future__ import annotations

from typing import Any

from dyatel.dyatel_play.play_checkbox import PlayCheckbox
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_checkbox import CoreCheckbox as SelCheckbox
from dyatel.dyatel_sel.core.core_driver import CoreDriver


class Checkbox(SelCheckbox, PlayCheckbox):
    """ Checkbox object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str, locator_type='', name='', parent: Any = None, wait=False, by_attr=False):
        """
        Initializing of checkbox based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of checkbox. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of checkbox (will be attached to logs)
        :param parent: parent of checkbox. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param by_attr: Selenium only: get is_checked state by custom attribute
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait
        self.by_attr = by_attr
        self.wrapped_element = None
        self._initialized = False

        self.element_class = self.__get_checkbox_class()
        if self.element_class:
            super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait,
                             by_attr=by_attr)

    def __get_checkbox_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        if PlayDriver.driver:
            Checkbox.__bases__ = PlayCheckbox,
            return PlayCheckbox
        elif CoreDriver.driver and CoreDriver.mobile:
            Checkbox.__bases__ = SelCheckbox,
            return SelCheckbox
        elif CoreDriver.driver and not CoreDriver.mobile:
            Checkbox.__bases__ = SelCheckbox,
            return SelCheckbox
