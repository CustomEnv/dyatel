from __future__ import annotations

from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.mixins import internal_utils


class PreviousObjectDriver:

    def set_driver_from_previous_object_for_page_or_group(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for group/page from previous object

        :param current_obj: group or page object
        :param frame_index: frame start index
        :return: None
        """
        if len(current_obj.driver_wrapper.all_drivers) > 1:
            if current_obj.driver == DriverWrapper.driver:
                previous_object = self._get_correct_previous_object(frame_index)
                if previous_object:
                    try:
                        current_obj.set_driver(previous_object.driver_wrapper)
                    except AttributeError:
                        return None

    def set_driver_from_previous_object_for_element(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for element from previous object

        :param current_obj: element object
        :param frame_index: frame start index
        :return: None
        """
        from dyatel.base.group import Group

        if len(current_obj.driver_wrapper.all_drivers) > 1:
            if current_obj.driver == DriverWrapper.driver:
                if not isinstance(current_obj, Group):
                    previous_object = self._get_correct_previous_object(frame_index, is_element=True)
                    if previous_object:
                        try:
                            current_obj.driver_wrapper = previous_object.driver_wrapper
                        except AttributeError:
                            pass

    def set_parent_from_previous_object_for_element(self, current_obj: Any, frame_index: int) -> None:
        """
        Set parent for element from previous object

        :param current_obj: element object
        :param frame_index: frame start index
        :return: None
        """
        from dyatel.base.group import Group
        from dyatel.base.element import Element
        from dyatel.base.checkbox import Checkbox

        if isinstance(current_obj, (Element, Checkbox)):
            previous_object = self._get_correct_previous_object(frame_index, is_element=True)
            if previous_object:
                if isinstance(previous_object, Group):
                    current_obj.parent = previous_object

    def previous_object_is_not_group_or_page(self, obj: Any) -> bool:
        """
        Check is previous object is npt group or page

        :param obj: obj to be checked
        :return: bool
        """
        from dyatel.base.group import Group
        from dyatel.base.page import Page

        is_group = isinstance(obj, Group)
        is_page = isinstance(obj, Page)
        return not (is_page or is_group) or obj is None

    def _get_correct_previous_object(self, index: int, is_element: bool = False) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param index: frame index to start
        :return: None or object with driver_wrapper
        """
        frame = internal_utils.get_frame(index)
        prev_object = frame.f_locals.get('self', None)
        unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        def get_driver(obj):
            return getattr(obj, 'driver', False)

        while (unexpected_previous_obj or get_driver(prev_object) == DriverWrapper.driver) and index < 15:

            if is_element:
                return None

            index += 1
            frame = internal_utils.get_frame(index)
            prev_object = frame.f_locals.get('self', None)
            unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        if frame.f_code.co_name == '__init__':
            return None

        return prev_object
