from __future__ import annotations

import os
import time
import platform
from copy import copy
from typing import List, Any, Union
from inspect import currentframe

from PIL import Image

from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.internal_utils import get_child_elements_with_names
from dyatel.visual_comparison import assert_same_images


class ElementMixin(DriverMixin):
    """ Mixin for PlayElement and CoreElement """

    def __enter__(self):
        self.name = None
        self.get_screenshot = None
        self.scroll_into_view = None

    def get_element_logging_data(self, element: Any = None) -> str:
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

    def assert_screenshot(self, filename: str = '', test_name: str = '', threshold: Union[int, float] = 0,
                          delay: Union[int, float] = 0.5, scroll: bool = False) -> ElementMixin:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :return: self
        """
        filename = filename if filename else self._get_screenshot_name(test_name)
        root_path = os.environ.get('visual', '')

        if not root_path:
            raise Exception('Provide visual regression path to environment. Example: os.environ["visual"] = "tests"')

        root_path = root_path if root_path.endswith('/') else f'{root_path}/'
        reference_directory = f'{root_path}reference/'
        output_directory = f'{root_path}output/'

        reference_file = f'{reference_directory}{filename}.png'

        os.makedirs(os.path.dirname(output_directory), exist_ok=True)
        os.makedirs(os.path.dirname(reference_directory), exist_ok=True)

        if scroll:
            self.scroll_into_view()

        time.sleep(delay)

        try:
            Image.open(reference_file)
        except FileNotFoundError:
            self.get_screenshot(reference_file)
            message = 'Reference file not found, but its just saved. ' \
                      'If it CI run, then you need to commit reference files.'
            raise FileNotFoundError(message) from None

        output_file = f'{output_directory}{filename}.png'
        self.get_screenshot(output_file)
        assert_same_images(output_file, reference_file, filename, threshold)
        return self

    def _get_screenshot_name(self, test_function_name: str = '') -> str:
        """
        Get screenshot name

        :param test_function_name: execution test name. Will try to find it automatically if empty string given
        :return: custom screenshot filename:
          :::
          - playwright: test_screenshot_rubik_s_cube_darwin_v_12_3_1_playwright_chromium
          - selenium: test_screenshot_rubik_s_cube_darwin_v_12_3_1_selenium_chrome
          - appium ios: test_screenshot_rubik_s_cube_iphone_13_v_15_4_appium_safari
          - appium android: test_screenshot_rubik_s_cube_pixel5_v_12_appium_chrome
          :::
        """
        if not test_function_name:
            back_frame = currentframe().f_back

            try:
                for _ in range(50):
                    if 'test' not in test_function_name and 'test' not in back_frame.f_code.co_filename:
                        back_frame = back_frame.f_back
                        test_function_name = back_frame.f_code.co_name
                    else:
                        break
            except AttributeError:
                raise Exception("Can't find test name. Please pass the test_name as parameter to assert_screenshot")
        else:
            test_function_name = test_function_name.replace('[', '').replace(']', '')

        element_name = self.name.replace('"', '').replace("'", '_')

        current_os = platform.system()
        if 'darwin' in current_os.lower():
            current_os += f'_v_{platform.mac_ver()[0]}'

        if self.driver_wrapper.mobile:
            caps = self.driver.caps
            device_name = caps['deviceName'] if self.driver_wrapper.is_ios else caps['avd']
            browser_name = caps['browserName']
            platform_version = caps['platformVersion']
            screenshot_name = f'{device_name}_v_{platform_version}_appium_{browser_name}'
        elif self.driver_wrapper.selenium:
            caps = self.driver.caps
            browser_name = caps['browserName']
            screenshot_name = f'{current_os}_selenium_{browser_name}'
        elif self.driver_wrapper.playwright:
            caps = self.driver_wrapper.instance
            screenshot_name = f'{current_os}_playwright_{caps.browser_type.name}'
        else:
            raise DriverWrapperException('Cant find current platform')

        screenshot_name = f'{test_function_name}_{element_name}_{screenshot_name}'
        screenshot_name = screenshot_name.replace(' ', '_').replace('.', '_').lower()
        return screenshot_name

    def _get_all_elements(self, sources: Union[tuple, list], instance_class: type) -> List[Any]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :param instance_class: attribute class to looking for
        :return: list of wrapped elements
        """
        wrapped_elements = []

        for element in sources:
            wrapped_object = copy(self)
            wrapped_object.element = element
            self.__set_parent_for_attr(instance_class, wrapped_object)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    def __set_parent_for_attr(self, instance_class: type, base_obj: object):
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
