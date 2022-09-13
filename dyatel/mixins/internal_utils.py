from __future__ import annotations

import inspect
from typing import Any

from dyatel.js_scripts import get_element_position_on_screen_js

WAIT_EL = 10
WAIT_PAGE = 20


all_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link', 'header', 'div',
            'textarea', 'svg', 'circle', 'iframe']


def initialize_objects_with_args(objects: list):
    """
    Initializing objects with itself args/kwargs

    :param objects: list of objects to initialize
    :return: None
    """
    for obj in objects:
        if not getattr(obj, '_initialized'):
            obj.__init__(**get_object_kwargs(obj))


def get_object_kwargs(obj: object):
    """
    Get actual args/kwargs of object __init__

    :param obj: object instance
    :return: object kwargs
    """
    init_args = inspect.getfullargspec(obj.__init__).args

    for index, key in enumerate(init_args):
        if key == 'self':
            init_args.pop(index)

    return {item: getattr(obj, item) for item in init_args}


def get_timeout_in_ms(timeout: int):
    """
    Get timeout in milliseconds for playwright

    :param timeout: timeout in seconds
    :return: timeout in milliseconds
    """
    return timeout * 1000 if timeout < 1000 else timeout


def get_child_elements(obj: object, instance: type) -> list:
    """
    Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    return list(get_child_elements_with_names(obj, instance).values())


def get_child_elements_with_names(obj: object, instance: type) -> dict:
    """
    Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements, class_items = {}, []

    for parent_class in obj.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    class_items += list(list(obj.__class__.__dict__.items()) + list(obj.__dict__.items()))

    for attribute, value in class_items:
        if isinstance(value, instance):
            if attribute != 'parent':
                elements.update({attribute: value})

    return elements


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
    el_rect = element.get_rect()
    ex, ey, ew, eh = el_rect['x'], el_rect['y'], el_rect['width'], el_rect['height']
    emx, emy = ex + ew / 2, ey + eh / 2  # middle of element

    if x:
        x = x + emx + ew / 2 if x > 0 else emx + x - ew / 2
    else:
        x = emx

    if y:
        y = y + emy + eh / 2 if y > 0 else emy + y - eh / 2
    else:
        y = emy

    return int(x), int(y)
