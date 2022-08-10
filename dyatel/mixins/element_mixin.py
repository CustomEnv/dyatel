from __future__ import annotations

import os
import time
from copy import copy
from typing import List, Any, Union

from PIL import Image

from dyatel.mixins.internal_utils import get_child_elements_with_names
from dyatel.visual_comparison import assert_same_images


class ElementMixin:
    """ Mixin for PlayElement and CoreElement """

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

    def assert_screenshot(self, filename: str, threshold: Union[int, float] = 0,
                          delay: Union[int, float] = 0.5) -> ElementMixin:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: screenshot path/name
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :return: current driver instance (Web/Mobile/PlayDriver)
        """
        root_path = os.environ.get('visual', '')

        if not root_path:
            raise Exception('Provide visual regression path. Example: os.environ["visual"] = "tests/visual"')

        root_path = root_path if root_path.endswith('/') else f'{root_path}/'
        reference_file = f'{root_path}reference/{filename}.png'
        get_screenshot = getattr(self, 'get_screenshot')

        try:
            Image.open(reference_file)
        except FileNotFoundError:
            get_screenshot(reference_file)
            message = 'Reference file not found, but its just saved. ' \
                      'If it CI run, then you need to commit reference files.'
            raise FileNotFoundError(message) from None

        time.sleep(delay)
        output_file = f'{root_path}output/{filename}.png'
        get_screenshot(output_file)
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
