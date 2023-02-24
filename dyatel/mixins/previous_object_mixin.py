from __future__ import annotations

from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.mixins import internal_utils
from dyatel.mixins.core_mixin import all_mid_level_elements


class PreviousObjectDriver:

    def set_driver_from_previous_object_for_page_or_group(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for group/page from previous object

        :param current_obj: group or page object
        :param frame_index: frame start index
        :return: None
        """
        if len(DriverWrapper.all_drivers) > 1:
            if current_obj.driver == DriverWrapper.driver:
                previous_object = self._get_correct_previous_object_with_driver(frame_index, current_obj=current_obj)
                if previous_object:
                    current_obj.driver_wrapper = previous_object.driver_wrapper

    def set_driver_from_previous_object_for_element(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for element from previous object

        :param current_obj: element object
        :param frame_index: frame start index
        :return: None
        """
        if len(DriverWrapper.all_drivers) > 1:
            if current_obj.driver == DriverWrapper.driver:
                if self._is_element(current_obj):
                    previous_object = self._get_correct_previous_object_with_driver(frame_index, current_obj=current_obj)
                    if previous_object:
                        current_obj.driver_wrapper = previous_object.driver_wrapper

    def set_parent_from_previous_object_for_element(self, current_obj: Any, frame_index: int) -> None:
        """
        Set parent for element from previous object

        :param current_obj: element object
        :param frame_index: frame start index
        :return: None
        """
        if not self._is_group(current_obj) and self._is_element(current_obj):
            previous_object = self._get_correct_previous_object_with_parent(frame_index)
            if previous_object:
                if self._is_group(previous_object):
                    current_obj.parent = previous_object

    def previous_object_is_not_group_or_page(self, obj: Any) -> bool:
        """
        Check is previous object is npt group or page

        :param obj: obj to be checked
        :return: bool
        """
        is_group = self._is_group(obj)
        is_page = self._is_page(obj)
        return not (is_page or is_group) or obj is None

    def _get_correct_previous_object_with_driver(self, index: int, current_obj: Any = False) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param index: frame index to start
        :return: None or object with driver_wrapper
        """
        timeout = 15
        frame = internal_utils.get_frame(index)
        prev_object = frame.f_locals.get('self', None)
        unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        def get_driver(obj):
            return getattr(obj, 'driver', False)

        while (unexpected_previous_obj or get_driver(prev_object) == DriverWrapper.driver) and index < timeout:
            index += 1

            if current_obj and prev_object:
                if str(current_obj) in str(vars(prev_object)) and current_obj != prev_object:
                    return None

            if index == timeout:
                return None

            frame = internal_utils.get_frame(index)
            prev_object = frame.f_locals.get('self', None)
            unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        if frame.f_code.co_name == '__init__':
            return None

        return prev_object

    def _get_correct_previous_object_with_parent(self, index: int) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param index: frame index to start
        :return: None or object with driver_wrapper
        """
        frame = internal_utils.get_frame(index)
        prev_object = frame.f_locals.get('self', None)

        if self._is_group(prev_object):
            return prev_object

        return None

    def _is_page(self, obj):
        return getattr(obj, '_is_page', False)

    def _is_element(self, obj):
        return getattr(obj, '_is_element', False)

    def _is_group(self, obj):
        return getattr(obj, '_is_group', False)


