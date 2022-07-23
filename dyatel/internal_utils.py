from __future__ import annotations

import os
import inspect
from copy import copy
from typing import Union, List, Any

from PIL import Image
from playwright.sync_api import Locator as PlaywrightWebElement
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.webelement import WebElement as AppiumWebElement

from dyatel.visual_comparison import assert_same_images


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


class Mixin:
    """ Mixin for PlayElement and CoreElement """
    name = None  # variable placeholder
    parent = None  # variable placeholder
    locator: str = ''  # variable placeholder
    locator_type: str = ''  # variable placeholder
    get_screenshot = None  # variable placeholder  #TODO: replace with get_attr in code
    element: Union[SeleniumWebElement, AppiumWebElement, PlaywrightWebElement] = None   # variable placeholder

    def get_element_logging_data(self, element=None) -> str:
        """
        Get full loging data depends on parent element

        :param element: element to collect log data
        :return: log string
        """
        element = element if element else self
        parent = element.parent
        current_data = f'Selector: ["{element.locator_type}": "{element.locator}"]'
        if parent:
            parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
            current_data = f'{current_data}. {parent_data}'
        return current_data

    def assert_screenshot(self, filename, threshold=0) -> Mixin:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: screenshot path/name
        :param threshold: possible threshold
        :return: current driver instance (Web/Mobile/PlayDriver)
        """
        root_path = os.environ.get('visual', '')
        reference_file = f'{root_path}/reference/{filename}.png'

        try:
            Image.open(reference_file)
        except FileNotFoundError:
            self.get_screenshot(reference_file)
            message = 'Reference file not found, but its just saved. ' \
                      'If it CI run, then you need to commit reference files.'
            raise FileNotFoundError(message) from None

        output_file = f'{root_path}/output/{filename}.png'
        self.get_screenshot(output_file)
        assert_same_images(output_file, reference_file, filename, threshold)
        return self

    def _get_all_elements(self, sources, instance_class) -> List[Any]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :param instance_class: attribute class to looking for
        :return: wrapped elements
        """
        wrapped_elements = []

        for element in sources:
            wrapped_object = copy(self)
            wrapped_object.element = element
            self.__set_parent_for_attr(instance_class, wrapped_object)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    def __set_parent_for_attr(self, instance_class, base_obj):
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


class DriverMixin:

    @property
    def driver(self):
        """
        Get source driver instance

        :return: SeleniumWebDriver for web test or AppiumWebDriver for mobile tests
        """
        return self._driver_instance.driver

    @property
    def driver_wrapper(self):
        """
        Get source driver wrapper instance

        :return: CoreDriver
        """
        return self._driver_instance.driver_wrapper

    def _set_driver(self, driver_wrapper, instance_class):
        """

        """
        new_driver = copy(self.driver_wrapper)
        setattr(new_driver, 'driver', copy(self.driver_wrapper.driver))
        setattr(new_driver, 'driver_wrapper', copy(self.driver_wrapper))

        new_driver.driver = driver_wrapper.driver
        new_driver.driver_wrapper = driver_wrapper

        self._driver_instance = new_driver
        self.__set_driver_for_attr(instance_class, self, new_driver)
        self.page_elements = get_child_elements(self, instance_class)

    def __set_driver_for_attr(self, instance_class, base_obj, driver_wrapper):
        """

        """
        child_elements = get_child_elements_with_names(base_obj, instance_class).items()

        for name, child in child_elements:
            wrapped_child = copy(child)
            wrapped_child._driver_instance = driver_wrapper
            setattr(base_obj, name, wrapped_child)
            self.__set_driver_for_attr(instance_class, wrapped_child, driver_wrapper)

        return self
