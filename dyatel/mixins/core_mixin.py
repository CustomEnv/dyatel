from __future__ import annotations

import sys
import inspect
from copy import copy
from typing import Any, Union

from appium.webdriver.common.appiumby import AppiumBy

WAIT_EL = 10
WAIT_PAGE = 15

all_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link', 'header', 'div',
            'textarea', 'svg', 'circle', 'iframe', 'label', 'tr', 'th', 'table', 'tbody', 'td', 'select', 'nav', 'li',
            'form', 'footer', 'frame', 'area', 'span'}


__statics = {}


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


def is_element(obj: Any) -> bool:
    return getattr(obj, '_object', None) == 'element'


def is_group(obj: Any) -> bool:
    return getattr(obj, '_object', None) == 'group'


def is_page(obj: Any) -> bool:
    return getattr(obj, '_object', None) == 'page'


def safe_setter(obj: Any, var: str, value: Any):
    if not hasattr(obj, var):
        setattr(obj, var, value)


def set_static(obj: Any) -> None:
    """
    Set static attributes for given object from base class

    :param obj: object to set static attributes
    :return: None
    """
    cls = obj._base_cls  # noqa
    scls = obj._scls  # noqa

    if cls not in __statics.keys():
        child_static = get_child_elements_with_names(cls).items()
        data = {name: value for name, value in child_static if name not in scls.__dict__.keys()}
        __statics.update({cls: data.items()})

    for name, item in __statics[cls]:
        setattr(obj.__class__, name, item)


def initialize_objects(current_object, objects: dict):
    """
    Copy objects ant initializing them with driver_wrapper from current object

    :param current_object: list of objects to initialize
    :param objects: list of objects to initialize
    :return: None
    """
    for name, obj in objects.items():
        set_name_for_attr(obj, name)
        copied_obj = copy(obj)
        promote_parent_element(copied_obj, current_object)
        setattr(current_object, name, copied_obj(driver_wrapper=current_object.driver_wrapper))
        initialize_objects(copied_obj, get_child_elements_with_names(copied_obj, all_mid_level_elements()))


def set_name_for_attr(attr, name):
    if not attr.name:
        attr.name = name.replace('_', ' ')


def set_parent_for_attr(base_obj: object, instance_class: Union[type, tuple], with_copy: bool = False):
    """
    Sets parent for all Elements/Group of given class.
    Should be called ONLY in Group object or all_elements method.
    Copy of objects will be executed if with_copy is True. Required for all_elements method

    :param instance_class: attribute class to looking for
    :param base_obj: object of attribute
    :param with_copy: copy child object or not
    :return: self
    """
    child_elements = get_child_elements_with_names(base_obj, instance_class).items()

    for name, child in child_elements:
        if with_copy:
            child = copy(child)

        if (is_group(base_obj) and child.parent is None) or is_group(child.parent):
            child.parent = base_obj

        if with_copy:
            setattr(base_obj, name, child)

        set_parent_for_attr(child, instance_class, with_copy)


def promote_parent_element(obj: Any, base_obj: Any):
    """
    Promote parent object in Element if parent is another Element

    :param obj: any element
    :param base_obj: base object of element: Page/Group instance
    :return: None
    """
    initial_parent = getattr(obj, 'parent', None)

    if not initial_parent:
        return None

    if is_element(initial_parent) and initial_parent != base_obj:
        for el in get_child_elements(base_obj, all_mid_level_elements()):
            if obj.parent.__base_obj_id == el.__base_obj_id:
                obj.parent = el


def get_child_elements(obj: object, instance: Union[type, tuple]) -> list:
    """
    Return objects of this object by instance

    :returns: list of page elements and page objects
    """
    return list(get_child_elements_with_names(obj, instance).values())


def get_child_elements_with_names(obj: Any, instance: Union[type, tuple] = None) -> dict:
    """
    Return all objects of given object or by instance
    Removing parent attribute from list to avoid infinite recursion and all dunder attributes

    :returns: list of page elements and page objects
    """
    elements = {}

    for attribute, value in get_all_attributes_from_object(obj).items():
        if instance and isinstance(value, instance) or not instance:
            if attribute != 'parent' and not attribute.startswith('__') and not attribute.endswith('__'):
                elements.update({attribute: value})

    return elements


def get_all_attributes_from_object(reference_obj: Any) -> dict:
    """
    Get attributes from given object and all its bases

    :param reference_obj: reference object
    :return: dict of all attributes
    """
    items = {}

    if not reference_obj:
        return items

    reference_class = reference_obj if inspect.isclass(reference_obj) else reference_obj.__class__
    all_bases = list(inspect.getmro(reference_class))
    all_bases.reverse()  # Reverse needed for getting child classes attributes first
    all_bases.remove(object)

    for parent_class in all_bases:
        str_parent_class = str(parent_class)

        if 'dyatel.base' not in str_parent_class and 'dyatel' in str_parent_class:
            continue

        items.update(dict(parent_class.__dict__))

    return {**items, **get_attributes_from_object(reference_obj)}


def get_attributes_from_object(reference_obj: Any) -> dict:
    """
    Get attributes from given object

    :param reference_obj:
    :return:
    """
    items = {}

    if not reference_obj:
        return items

    if not inspect.isclass(reference_obj):
        items.update(dict(reference_obj.__class__.__dict__))

    items.update(dict(reference_obj.__dict__))

    return items


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
    Get driver with index caption for logging

    :param driver_wrapper: driver wrapper object
    :param driver: driver object
    :return: '1_driver' or '2_driver' etc.
    """
    try:
        index = driver_wrapper.all_drivers.index(driver) + 1
    except (ValueError, AttributeError):
        index = '?'

    return f'{index}_driver'


def all_mid_level_elements() -> tuple:
    """
    Get all mid level elements. Workaround for circular import

    :return: tuple of mid level elements.
    """
    from dyatel.dyatel_play.play_element import PlayElement
    from dyatel.dyatel_sel.elements.mobile_element import MobileElement
    from dyatel.dyatel_sel.elements.web_element import WebElement

    return WebElement, MobileElement, PlayElement


def get_element_info(element: Any) -> str:
    """
    Get element selector information with parent object selector if it exists

    :param element: element to collect log data
    :return: log string
    """
    parent = element.parent
    current_data = f'Selector: ["{element.locator_type}": "{element.locator}"]'
    if parent:
        parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
        current_data = f'{current_data}. {parent_data}'
    return current_data


all_locator_types = get_child_elements(AppiumBy, str)
