from __future__ import annotations

import inspect

WAIT_EL = 10
WAIT_PAGE = 20


all_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link', 'header', 'div',
            'textarea', ]


def initialize_objects_with_args(objects: list):
    """
    Initializing objects with itself args/kwargs

    :param objects: list of objects to initialize
    :return: None
    """
    for obj in objects:
        if not getattr(obj, '_initialized'):
            obj.__init__(**get_object_kwargs(obj))


def get_object_kwargs(obj):
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


def get_child_elements(self, instance) -> list:
    """
    Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    return list(get_child_elements_with_names(self, instance).values())


def get_child_elements_with_names(self, instance) -> dict:
    """
    Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements, class_items = {}, []

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    class_items += list(list(self.__class__.__dict__.items()) + list(self.__dict__.items()))

    for attribute, value in class_items:
        if isinstance(value, instance):
            if attribute != 'parent':
                elements.update({attribute: value})

    return elements


def calculate_coordinate_to_click(element, x, y):
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
    :return:  coordinates
    """
    element_size = element.element.size
    half_width, half_height = element_size['width'] / 2, element_size['height'] / 2
    dx, dy = half_width, half_height
    if x:
        dx += x + (-half_width if x < 0 else half_width)
    if y:
        dy += -y + (half_height if y < 0 else -half_height)
    return dx, dy