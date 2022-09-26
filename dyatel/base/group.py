from __future__ import annotations

import copy
from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.internal_utils import get_child_elements_with_names


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

    def __init__(self, locator: str, locator_type: str = '', name: str = '',
                 parent: Any = None, wait: bool = False, driver_wrapper: Union[DriverWrapper, Any] = None, **kwargs):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        """
        self._init_locals = locals()
        super().__init__(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)
        # it's necessary to leave it after init
        if driver_wrapper:
            self._driver_instance = get_driver_wrapper_from_object(self, driver_wrapper)
            self.set_driver(self._driver_instance)

    def __repr__(self, base_class=None):
        return super().__repr__(self.__class__.__base__.__base__.__base__.__name__)

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
        for name, value in get_child_elements_with_names(self, Element).items():
            if not value.parent:
                setattr(self, name, copy.copy(value))
                value = getattr(self, name)
                value.parent = self
