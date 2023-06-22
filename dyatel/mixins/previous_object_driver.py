from __future__ import annotations

import os
from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.utils.internal_utils import get_frame, is_group, is_page, is_element


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
                if is_element(current_obj):
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
        if not is_group(current_obj) and is_element(current_obj):
            previous_object = self._get_correct_previous_object_with_parent(frame_index)
            if previous_object:
                if is_group(previous_object):
                    current_obj.parent = previous_object

    def previous_object_is_not_group_or_page(self, obj: Any) -> bool:
        """
        Check is previous object is npt group or page

        :param obj: obj to be checked
        :return: bool
        """
        return not (is_group(obj) or is_page(obj)) or obj is None

    def _get_correct_previous_object_with_driver(self, index: int, current_obj: Any = False) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param index: frame index to start
        :return: None or object with driver_wrapper
        """
        timeout = 15
        frame = get_frame(index)
        prev_object = self._get_self_object(frame)
        unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        while (unexpected_previous_obj or self._get_driver(prev_object) == DriverWrapper.driver) and index < timeout:

            if index == timeout or self._is_test_function(frame):
                return None

            if current_obj and prev_object:
                if str(current_obj) in str(vars(prev_object)) and current_obj != prev_object:
                    return None

            index += 1
            frame = get_frame(index)
            prev_object = self._get_self_object(frame)
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
        prev_object = self._get_self_object(get_frame(index))

        if is_group(prev_object):
            return prev_object

        return None

    @staticmethod
    def _get_driver(obj):
        return getattr(obj, 'driver', False)

    @staticmethod
    def _is_test_function(frame):
        return frame.f_code.co_name in os.environ['PYTEST_CURRENT_TEST']

    @staticmethod
    def _get_self_object(frame):
        return frame.f_locals.get('self', None)
