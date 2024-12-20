from __future__ import annotations

from functools import lru_cache
from typing import Any

from appium.webdriver.common.appiumby import AppiumBy

from dyatel.utils.internal_utils import (
    get_child_elements_with_names,
    get_child_elements,
    get_all_attributes_from_object,
)


all_locator_types = get_child_elements(AppiumBy, str)
available_kwarg_keys = ('desktop', 'mobile', 'ios', 'android')


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

@lru_cache(maxsize=16)
def get_static(cls: Any):
    return get_child_elements_with_names(cls).items()

class InternalMixin:

    @staticmethod
    def _check_kwargs(kwargs):
        assert all(item in available_kwarg_keys for item in kwargs), \
            f'The given kwargs is not available. Please provide them according to available keys: {available_kwarg_keys}'

    def _safe_setter(self, var: str, value: Any):
        if not hasattr(self, var):
            setattr(self, var, value)

    def _set_static(self: Any, cls) -> None:
        """
        Set static from base cls (Web/Mobile/Play Element/Page etc.)

        :return: None
        """
        data = {
            name: value for name, value in get_static(cls)
            if name not in get_all_attributes_from_object(self).keys()
        }.items()

        for name, item in data:
            setattr(self.__class__, name, item)

    def _repr_builder(self: Any):
        class_name = self.__class__.__name__
        obj_id = hex(id(self))
        parent = getattr(self, 'parent', False)

        try:
            parent_class = self.parent.__class__.__name__ if parent else None
            locator_holder = getattr(self, 'anchor', self)

            locator = f'locator="{locator_holder.locator}"'
            locator_type = f'locator_type="{locator_holder.locator_type}"'
            name = f'name="{self.name}"'
            parent = f'parent={parent_class}'
            driver = f'{self.driver_wrapper.label}={self.driver}'

            base = f'{class_name}({locator}, {locator_type}, {name}, {parent}) at {obj_id}'
            additional_info = driver
            return f'{base}, {additional_info}'
        except AttributeError:
            return f'{class_name} object at {obj_id}'
