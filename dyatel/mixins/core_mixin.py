from __future__ import annotations

import sys
import inspect
from copy import copy
from typing import Any, Union

WAIT_EL = 10
WAIT_PAGE = 15

all_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link', 'header', 'div',
            'textarea', 'svg', 'circle', 'iframe', 'label', 'tr', 'th', 'table', 'tbody', 'td', 'select', 'nav', 'li',
            'form', 'footer', 'frame', 'area', 'span'}


def get_frame(frame=1):
    """
    Get frame by given id

    :param frame: frame id, "current" by default
    :return: frame
    """
    return sys._getframe(frame)  # noqa


def get_timeout_in_ms(timeout: int):
    """
    Get timeout in milliseconds for playwright

    :param timeout: timeout in seconds
    :return: timeout in milliseconds
    """
    return timeout * 1000 if timeout < 1000 else timeout


def initialize_objects(current_object, objects: dict):
    """
    Initializing objects with itself args/kwargs

    :param current_object: list of objects to initialize
    :param objects: list of objects to initialize
    :return: None
    """
    for name, obj in objects.items():
        if not getattr(obj, '_initialized', False):
            copied_obj = copy(obj)
            setattr(current_object, name, copied_obj(driver_wrapper=current_object.driver_wrapper))
            initialize_objects(obj, get_child_elements_with_names(obj, all_mid_level_elements()))


def get_child_elements(obj: object, instance: Union[type, tuple]) -> list:
    """
    Return objects of this object by instance

    :returns: list of page elements and page objects
    """
    return list(get_child_elements_with_names(obj, instance).values())


def get_child_elements_with_names(obj: Any, instance: Union[type, tuple]) -> dict:
    """
    Return objects of this object by instance

    :returns: list of page elements and page objects
    """
    elements = {}

    for attribute, value in get_all_attributes_from_object(obj).items():
        if isinstance(value, instance):
            if attribute != 'parent' and '__' not in attribute:
                elements.update({attribute: value})

    return elements


def get_all_attributes_from_object(
        reference_obj: Any,
        stop_on_base: bool = False
) -> dict:
    """
    Get all attributes from object

    :param reference_obj: reference object
    :param stop_on_base: stop grabbing on dyatel base classes ~ WebElement/PlayPage etc.
    :return: dict of all attributes
    """
    reference_class = reference_obj if inspect.isclass(reference_obj) else reference_obj.__class__

    def get_items(cls, items=None):

        if not items:
            items = {}

        for parent_class in cls.__bases__:

            str_parent_class = str(parent_class)

            if "'object'" in str_parent_class or "'type'" in str_parent_class:
                break

            if stop_on_base and 'dyatel' in str_parent_class and 'dyatel.base' not in str_parent_class:
                continue

            items.update({name: value for name, value in parent_class.__dict__.items() if name not in items.keys()})

            get_items(parent_class, items)

        return items

    obj_items = get_items(reference_class)
    obj_items.update({attr: value for attr, value in reference_class.__dict__.items() if '__' not in str(attr)})
    obj_items.update(dict(reference_obj.__dict__))

    return obj_items


def is_target_on_screen(x: int, y: int, possible_range: dict):
    """
    Check is given coordinates fit into given range

    :param x: x coordinate
    :param y: y coordinate
    :param possible_range: possible range
    :return: bool
    """
    is_x_on_screen = x in range(possible_range['width'])
    is_y_on_screen = y in range(possible_range['height'])
    return is_x_on_screen and is_y_on_screen


def calculate_coordinate_to_click(element: Any, x: int = 0, y: int = 0) -> tuple:
    """
    Calculate coordinates to click for element
    Examples:
        (0, 0) -- center of the element
        (5, 0) -- 5 pixels to the right
        (-10, 0) -- 10 pixels to the left out of the element
        (0, -5) -- 5 pixels below the element

    :param element: dyatel WebElement or MobileElement
    :param x: horizontal offset relative to either left (x < 0) or right side (x > 0)
    :param y: vertical offset relative to either top (y > 0) or bottom side (y < 0)
    :return: tuple of calculated coordinates
    """
    ey, ex, ew, eh = element.get_rect().values()
    mew, meh = ew / 2, eh / 2
    emx, emy = ex + mew, ey + meh  # middle of element

    sx, sy = ([-1, 1][s > 0] for s in [x, y])
    x = emx + bool(x) * (x + mew * sx)
    y = emy + bool(y) * (y + meh * sy)

    return int(x), int(y)


def driver_with_index(driver_wrapper, driver) -> str:
    """
    Get driver index for logging

    :param driver_wrapper: driver wrapper object
    :param driver: driver object
    :return: 'index_driver' data
    """
    try:
        index = driver_wrapper.all_drivers.index(driver) + 1
    except (ValueError, AttributeError):
        index = '?'

    return f'{index}_driver'


def all_mid_level_elements() -> tuple:
    from dyatel.dyatel_play.play_element import PlayElement
    from dyatel.dyatel_sel.elements.mobile_element import MobileElement
    from dyatel.dyatel_sel.elements.web_element import WebElement

    return WebElement, MobileElement, PlayElement


def get_element_info(element: Any) -> str:
    """
    Get full loging data depends on parent element

    :param element: element to collect log data
    :return: log string
    """
    parent = element.parent
    current_data = f'Selector: ["{element.locator_type}": "{element.locator}"]'
    if parent:
        parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
        current_data = f'{current_data}. {parent_data}'
    return current_data


def set_parent_for_attr(instance_class: Union[type, tuple], base_obj: object, check_parent: bool = False):
    """
    Copy attributes of given object and set new parent for him

    :param instance_class: attribute class to looking for
    :param base_obj: object of attribute
    :param check_parent: object of attribute
    :return: self
    """
    child_elements = get_child_elements_with_names(base_obj, instance_class).items()

    for name, child in child_elements:
        wrapped_child = copy(child)

        parent = wrapped_child.parent
        parent_object_type = getattr(parent, '_object', None)

        if parent_object_type == 'group' or parent is None:
            wrapped_child.parent = base_obj

        if parent_object_type == 'element' and not parent._initialized:  # noqa
            wrapped_child.parent = parent()  # noqa

        setattr(base_obj, name, wrapped_child)
        set_parent_for_attr(instance_class, wrapped_child, check_parent=check_parent)
