from __future__ import annotations

from copy import copy
from typing import Union, Any

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from playwright.sync_api import Page as PlaywrightWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.mixins.internal_utils import get_child_elements, get_child_elements_with_names, get_frame


def get_driver_wrapper_from_object(obj, custom_driver_wrapper_object: Union[DriverWrapper, Any]):
    """
    Get driver wrapper from custom object

    :param obj: self object of the class
    :param custom_driver_wrapper_object: custom object. Can be driver_wrapper or object with driver_wrapper
    :return: driver wrapper object
    """
    if isinstance(custom_driver_wrapper_object, (DriverWrapper, PlayDriver, WebDriver, MobileDriver)):
        new_driver_instance = custom_driver_wrapper_object
    elif hasattr(custom_driver_wrapper_object, 'driver_wrapper'):
        new_driver_instance = custom_driver_wrapper_object.driver_wrapper
    else:
        msg = f'Cant get custom driver_wrapper object for "{getattr(obj, "name")}" of "{obj.__class__}"'
        raise Exception(msg)

    return new_driver_instance


class DriverMixin:

    @property
    def driver(self) -> Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightWebDriver]:
        """
        Get source driver instance

        :return: SeleniumWebDriver/AppiumWebDriver/PlaywrightWebDriver
        """
        driver_instance = getattr(self, '_driver_instance', DriverWrapper)
        return driver_instance.driver

    @driver.setter
    def driver(self, driver: Union[SeleniumWebDriver, AppiumWebDriver, PlaywrightWebDriver]):
        """ Set source driver instance """
        setattr(self, '_driver_instance', driver)

    @property
    def driver_wrapper(self) -> Union[WebDriver, MobileDriver, PlayDriver, DriverWrapper]:
        """
        Get source driver wrapper instance

        :return: driver_wrapper
        """
        driver_instance = getattr(self, '_driver_instance', DriverWrapper)
        return driver_instance.driver_wrapper

    @driver_wrapper.setter
    def driver_wrapper(self, driver_wrapper: Union[WebDriver, MobileDriver, PlayDriver, DriverWrapper]):
        """ Set source driver wrapper instance """
        setattr(self, '_driver_instance', driver_wrapper)

    def _set_driver(self, driver_wrapper, instance_class) -> DriverMixin:
        """
        Set driver_wrapper/driver instances for class

        :param driver_wrapper: driver wrapper to be set
        :param instance_class: instance of attributes of the class
        :return: self
        """
        new_driver = copy(self.driver_wrapper)
        setattr(new_driver, 'driver', copy(self.driver_wrapper.driver))
        setattr(new_driver, 'driver_wrapper', copy(self.driver_wrapper))

        new_driver.driver = driver_wrapper.driver
        new_driver.driver_wrapper = driver_wrapper

        self._driver_instance = new_driver
        self.__set_driver_for_attr(self, instance_class, new_driver)
        self.page_elements = get_child_elements(self, instance_class)

        return self

    def __set_driver_for_attr(self, base_obj, instance_class, driver_wrapper) -> DriverMixin:
        """
        Set driver_wrapper/driver instances for attributes

        :param base_obj: class of attributes
        :param instance_class: instance of attributes to be changed
        :param driver_wrapper: driver wrapper to be set
        :return: self
        """
        child_elements = get_child_elements_with_names(base_obj, instance_class).items()

        for name, child in child_elements:
            wrapped_child = copy(child)
            wrapped_child._driver_instance = driver_wrapper
            setattr(base_obj, name, wrapped_child)

            if getattr(wrapped_child, 'parent', None):
                wrapped_child.parent._driver_instance = driver_wrapper

            self.__set_driver_for_attr(wrapped_child, instance_class, driver_wrapper)

        return self


class PreviousObjectDriver:

    def set_driver_from_previous_object_for_page(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for group/page from previous object

        :param current_obj: group or page object
        :param frame_index: frame start index
        :return: None
        """
        if current_obj.driver_wrapper:
            if len(current_obj.driver_wrapper.all_drivers) > 1:
                if current_obj.driver == DriverWrapper.driver:
                    previous_object = self._get_correct_previous_object(frame_index)
                    if previous_object:
                        try:
                            current_obj.set_driver(previous_object.driver_wrapper)
                        except AttributeError:
                            return None

    def set_driver_from_previous_object_for_element(self, current_obj: Any, frame_index: int) -> None:
        """
        Set driver for element from previous object

        :param current_obj: element object
        :param frame_index: frame start index
        :return: None
        """
        if current_obj.driver_wrapper:
            if len(current_obj.driver_wrapper.all_drivers) > 1:
                if current_obj.driver == DriverWrapper.driver:
                    previous_object = self._get_correct_previous_object(frame_index)
                    if previous_object:

                        if current_obj.parent is None:
                            from dyatel.base.group import Group
                            if isinstance(previous_object, Group):
                                current_obj.parent = previous_object

                        try:
                            current_obj.driver_wrapper = previous_object.driver_wrapper
                        except AttributeError:
                            pass

    def previous_object_is_not_group_or_page(self, obj: Any) -> bool:
        """
        Check is previous object is npt group or page

        :param obj: obj to be checked
        :return: bool
        """
        from dyatel.base.group import Group
        from dyatel.base.page import Page
        is_group = isinstance(obj, Group)
        is_page = isinstance(obj, Page)
        return not (is_page or is_group) or obj is None

    def _get_correct_previous_object(self, index: int) -> Union[None, Any]:
        """
        Finds previous object with nested element/group/page

        :param index: frame index to start
        :return: None or object with driver_wrapper
        """
        frame = get_frame(index)
        prev_object = frame.f_locals.get('self', None)
        unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        while unexpected_previous_obj and index < 10:
            if frame.f_code.co_name == '__init__':
                return None

            index += 1
            frame = get_frame(index)
            prev_object = frame.f_locals.get('self', None)
            unexpected_previous_obj = self.previous_object_is_not_group_or_page(prev_object)

        if frame.f_code.co_name == '__init__':
            return None

        return prev_object
