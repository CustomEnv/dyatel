def get_child_elements(self, instance):
    """Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements = []

    class_items = list(self.__dict__.items()) + list(self.__class__.__dict__.items())

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    for attribute, value in class_items:
        if isinstance(value, instance):
            elements.append(value)
    return set(elements)


def get_timeout(timeout):
    if timeout < 100:  # for timeout in ms
        timeout *= 1000
    return timeout


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


class AfterInitMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.after_init()
        return obj


class Mixin:
    parent = None
    locator = None
    locator_type = None

    def _get_element_logging_data(self, element=None):
        element = element if element else self
        parent = element.parent
        current_data = f'Selector: ["{element.locator_type}": "{element.locator}"]'
        if parent:
            parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
            current_data = f'{current_data}. {parent_data}'
        return current_data
