from __future__ import annotations

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.mixins.internal_utils import get_all_attributes_from_object, driver_with_index


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

        locator = f'locator="{instance.locator}"'
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
