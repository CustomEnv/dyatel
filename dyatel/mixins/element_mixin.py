from __future__ import annotations

from abc import abstractmethod
from copy import copy
from typing import List, Any, Union

from appium.webdriver.common.appiumby import AppiumBy

from dyatel.mixins.core_mixin import set_parent_for_attr, get_child_elements


all_locator_types = get_child_elements(AppiumBy, str)


class ElementMixin:
    """ Mixin for PlayElement and CoreElement """

    @property
    @abstractmethod
    def all_elements(self):
        raise NotImplementedError('all_elements method is not implemented for current class')

    @abstractmethod
    def wait_enabled(self, *args, **kwargs):
        raise NotImplementedError('wait_enabled method is not implemented for current class')

    @abstractmethod
    def wait_element_without_error(self, *args, **kwargs):
        raise NotImplementedError('wait_element_without_error method is not implemented for current class')

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
            set_parent_for_attr(wrapped_object, instance_class, with_copy=True)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements


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
