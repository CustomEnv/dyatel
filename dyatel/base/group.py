from __future__ import annotations

from typing import Any

from dyatel.base.driver import Driver
from dyatel.base.element import Element
from dyatel.internal_utils import get_child_elements


class AfterInitMeta(type):
    """ Call a custom function right after __init__ of original class """

    def __call__(cls, *args, **kwargs):
        """
        Wrapper for calling a custom function right after __init__ of original class

        :param args: original class args
        :param kwargs: original class kwargs
        :return: class object
        """
        obj = type.__call__(cls, *args, **kwargs)
        obj.customise_children()
        return obj


class Group(Element, metaclass=AfterInitMeta):
    """ Group of elements. Should be defined as class """

    def __init__(self, locator: str, locator_type='', name='', parent: Any = None, wait=False, driver_wrapper=None):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        """
        self.__custom_driver_wrapper = driver_wrapper
        super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    def set_driver(self, driver_wrapper) -> Group:
        """
        Set driver instance for group and elements

        :param driver_wrapper: driver wrapper object ~ Driver/WebDriver/MobileDriver/CoreDriver/PlayDriver
        :return: self
        """
        self._set_driver(driver_wrapper, Element)
        return self

    def customise_children(self):
        """
        Set parent and custom driver for Group class variables, if their instance is Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        for element in get_child_elements(self, Element):
            element.parent = self

        if self.__custom_driver_wrapper:
            if isinstance(self.__custom_driver_wrapper, Driver):
                self.set_driver(self.__custom_driver_wrapper)
            else:
                self.set_driver(self.__custom_driver_wrapper.driver_wrapper)
