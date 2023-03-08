from __future__ import annotations

from copy import copy
from typing import List, Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.core_mixin import (
    get_all_attributes_from_object,
    driver_with_index,
    get_element_info,
    set_parent_for_attr,
)


def shadow_class(current_cls):
    """
    Creates a "shadow" class from current one and base class of current

    :param current_cls: current class
    :return: new "shadow" class
    """
    if DriverWrapper.is_multiplatform:

        if not getattr(current_cls, '__created', False):
            class_objects = get_all_attributes_from_object(current_cls, stop_on_base=True)
            new_class = type(f'Shadow{current_cls.__name__}', (current_cls,), class_objects)
            new_class.__created = True
            return object.__new__(new_class)  # noqa

    return object.__new__(current_cls)


def repr_builder(instance):
    class_name = instance.__class__.__name__
    obj_id = hex(id(instance))

    try:
        driver_title = driver_with_index(instance.driver_wrapper, instance.driver)
        parent_class = instance.parent.__class__.__name__ if getattr(instance, 'parent', False) else None
        locator_holder = getattr(instance, 'anchor', instance)

        locator = f'locator="{locator_holder.locator}"'
        locator_type = f'locator_type="{locator_holder.locator_type}"'
        name = f'name="{instance.name}"'
        parent = f'parent={parent_class}'
        driver = f'{driver_title}={instance.driver}'

        base = f'{class_name}({locator}, {locator_type}, {name}, {parent}) at {obj_id}'
        additional_info = driver
        return f'{base}, {additional_info}'
    except AttributeError:
        return f'{class_name} object at {obj_id}'


def get_base_class(obj, current_cls):
    return obj.__class__ if DriverWrapper.is_multiplatform else current_cls


def set_base_class(obj, current_cls, cls_to_set):
    cls = get_base_class(obj, current_cls)

    if cls_to_set:
        cls.__bases__ = cls_to_set

    return cls


class ElementMixin(DriverMixin):
    """ Mixin for PlayElement and CoreElement """

    def get_element_info(self, element: Any = None) -> str:
        """
        Get full loging data depends on parent element

        :param element: element to collect log data
        :return: log string
        """
        element = element if element else self
        return get_element_info(element)

    def _get_all_elements(self, sources: Union[tuple, list], instance_class: type) -> List[Any]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :param instance_class: attribute class to looking for
        :return: list of wrapped elements
        """
        wrapped_elements = []

        for element in sources:
            wrapped_object: Any = copy(self)
            wrapped_object.element = element
            wrapped_object._wrapped = True
            set_parent_for_attr(instance_class, wrapped_object, with_copy=True)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements
