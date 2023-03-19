from __future__ import annotations

from typing import Any, Union, List

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.element_mixin import repr_builder
from dyatel.mixins.previous_object_driver import PreviousObjectDriver
from dyatel.mixins.core_mixin import (
    all_mid_level_elements,
    set_parent_for_attr,
    get_child_elements,
    initialize_objects,
    get_child_elements_with_names,
)


class Group(Element):
    """ Group of elements. Should be defined as class """

    _object = 'group'

    def __repr__(self):
        return repr_builder(self)

    def __init__(  # noqa
            self,
            locator: str = '',
            locator_type: str = '',
            name: str = '',
            parent: Union[Any, False] = None,
            wait: bool = None,
            driver_wrapper: Union[DriverWrapper, Any] = None,
            **kwargs
    ):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects of False for skip
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self._scls = Group
        self._init_locals = locals()
        self._driver_instance = get_driver_wrapper_from_object(driver_wrapper)

        super().__init__(
            locator=locator,
            locator_type=locator_type,
            name=name,
            parent=parent,
            wait=wait
        )

    def _modify_children(self):
        """
        Initializing of attributes with type == Group/Element.
        Required for classes with base == Group.
        """
        elements_types = all_mid_level_elements()

        initialize_objects(self, get_child_elements_with_names(self, elements_types))
        set_parent_for_attr(self, elements_types)
        self.child_elements: List[Element] = get_child_elements(self, elements_types)

    def _modify_object(self):
        """
        Modify current object. Required for Group that placed into functions:
        - set driver from previous object if previous driver different.
        """
        PreviousObjectDriver().set_driver_from_previous_object_for_page_or_group(self, 6)
