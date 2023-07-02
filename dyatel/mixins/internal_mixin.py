from functools import cache
from typing import Any

from dyatel.utils.internal_utils import get_child_elements_with_names


available_kwarg_keys = ('desktop', 'mobile', 'ios', 'android')


class InternalMixin:

    @staticmethod
    def _check_kwargs(kwargs):
        assert all(item in available_kwarg_keys for item in kwargs), \
            f'The given kwargs is not available. Please provide them according to available keys: {available_kwarg_keys}'

    @cache
    def __get_static(self, cls: Any):
        return get_child_elements_with_names(cls).items()

    def _safe_setter(self, var: str, value: Any):
        if not hasattr(self, var):
            setattr(self, var, value)

    def _set_static(self: Any, scls) -> None:
        """
        Set static attributes for given object from base class

        :param scls: root class of object
        :return: None
        """
        cls = self._base_cls

        for name, item in {name: value for name, value in self.__get_static(cls) if name not in scls.__dict__.keys()}.items():
            setattr(self.__class__, name, item)

    def _repr_builder(self: Any):
        class_name = self.__class__.__name__
        obj_id = hex(id(self))
        parent = getattr(self, 'parent', False)

        try:
            driver_title = self.driver.label
            parent_class = self.parent.__class__.__name__ if parent else None
            locator_holder = getattr(self, 'anchor', self)

            locator = f'locator="{locator_holder.locator}"'
            locator_type = f'locator_type="{locator_holder.locator_type}"'
            name = f'name="{self.name}"'
            parent = f'parent={parent_class}'
            driver = f'{driver_title}={self.driver}'

            base = f'{class_name}({locator}, {locator_type}, {name}, {parent}) at {obj_id}'
            additional_info = driver
            return f'{base}, {additional_info}'
        except AttributeError:
            return f'{class_name} object at {obj_id}'
