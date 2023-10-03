from __future__ import annotations

import inspect
from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapperSessions


def set_instance_frame(new_instance: Any) -> None:
    """
    Sets frame on element initialisation

    :param new_instance: object instance from __new__
    :return: None
    """
    if DriverWrapperSessions.sessions_count() >= 2:
        stack = inspect.stack()
        new_instance.frame = stack[2][0]


class PreviousObjectDriver:

    def set_driver_from_previous_object(self, current_obj: Any) -> None:
        """
        Set driver for given object from previous object

        :param current_obj: element object
        :return: None
        """
        if len(DriverWrapperSessions.all_sessions) >= 2:
            if current_obj.driver_wrapper == DriverWrapperSessions.first_session():
                previous_object = self._get_prev_obj_instance(current_obj=current_obj)
                if previous_object and getattr(previous_object, 'driver_wrapper', None):
                    current_obj.driver_wrapper = previous_object.driver_wrapper

    def _get_prev_obj_instance(self, current_obj: Any) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param current_obj: frame index to start
        :return: None or object with driver_wrapper
        """
        return current_obj.frame.f_locals.get('self', None)
