from __future__ import annotations

from copy import copy
from typing import List, Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.internal_utils import get_child_elements_with_names, get_platform_locator, driver_with_index, \
    get_all_attributes_from_object


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


def repr_builder(instance, cls):
    try:
        class_name = instance.__class__.__name__
        driver_title = driver_with_index(instance.driver_wrapper, instance.driver)
        parent_class = instance.parent.__class__.__name__ if hasattr(instance, 'parent') else None

        locator = f'locator="{get_platform_locator(instance)}"'
        locator_type = f'locator_type="{instance.locator_type}"'
        name = f'name="{instance.name}"'
        parent = f'parent={parent_class}'
        obj_id = hex(id(instance))
        driver = f'{driver_title}={instance.driver}'

        base = f'{class_name}({locator}, {locator_type}, {name}, {parent}) at {obj_id}'
        additional_info = driver
        return f'{base}, {additional_info}'
    except AttributeError:
        return super(get_base_class(instance, cls), instance).__repr__()


def all_mid_level_elements() -> tuple:
    from dyatel.dyatel_play.play_element import PlayElement
    from dyatel.dyatel_sel.elements.mobile_element import MobileElement
    from dyatel.dyatel_sel.elements.web_element import WebElement

    return WebElement, MobileElement, PlayElement


def get_base_class(obj, current_cls):
    return obj.__class__ if DriverWrapper.is_multiplatform else current_cls


def set_base_class(obj, current_cls, cls_to_set):
    cls = get_base_class(obj, current_cls)

    if cls_to_set:
        cls.__bases__ = cls_to_set

    return cls


def get_element_info(element: Any) -> str:
    """
    Get full loging data depends on parent element

    :param element: element to collect log data
    :return: log string
    """
    parent = element.parent
    current_data = f'Selector: ["{element.locator_type}": "{get_platform_locator(element)}"]'
    if parent:
        parent_data = f'Parent selector: ["{parent.locator_type}": "{get_platform_locator(parent)}"]'
        current_data = f'{current_data}. {parent_data}'
    return current_data


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
            self.__set_parent_for_attr(instance_class, wrapped_object)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    def __set_parent_for_attr(self, instance_class: type, base_obj: object):
        """
        Copy attributes of given object and set new parent for him

        :param instance_class: attribute class to looking for
        :param base_obj: object of attribute
        :return: self
        """
        child_elements = get_child_elements_with_names(base_obj, instance_class).items()

        for name, child in child_elements:
            wrapped_child = copy(child)
            wrapped_child.parent = base_obj
            setattr(base_obj, name, wrapped_child)
            self.__set_parent_for_attr(instance_class, wrapped_child)

        return self
