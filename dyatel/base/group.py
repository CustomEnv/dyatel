from __future__ import annotations

from typing import Any, Union, List

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.mixins.objects.locator import Locator
from dyatel.utils.internal_utils import (
    set_parent_for_attr,
    get_child_elements,
    initialize_objects,
    get_child_elements_with_names
)


class Group(Element):
    """ Group of elements. Should be defined as class """

    _object = 'group'

    def __repr__(self):
        return self._repr_builder()

    def __init__(
            self,
            locator: Union[Locator, str] = '',
            name: str = '',
            parent: Union[Any, False] = None,
            wait: bool = None,
            driver_wrapper: Union[DriverWrapper, Any] = None,
    ):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects of False for skip
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        """
        self._init_locals = locals()
        super().__init__(
            locator=locator,
            name=name,
            parent=parent,
            wait=wait,
            driver_wrapper=driver_wrapper,
        )

    def _modify_children(self) -> None:
        """
        Initializing of attributes with type == Group/Element.
        Required for classes with base == Group.
        """
        initialize_objects(self, get_child_elements_with_names(self, Element), Element)
        set_parent_for_attr(self, Element)
        self.child_elements: List[Element] = get_child_elements(self, Element)
