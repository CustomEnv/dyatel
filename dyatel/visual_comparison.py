from __future__ import annotations

import os
import time
import importlib
import json
import base64
import math
import operator
from functools import reduce
from typing import Union, List, Any
from string import punctuation

from PIL import Image, ImageChops

from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.log_mixin import autolog
from dyatel.mixins.internal_utils import get_frame


class VisualComparison:

    visual_regression_path = ''
    visual_reference_generation = False

    def __init__(self, driver_wrapper, element):
        self.driver_wrapper = driver_wrapper
        self.element = element

    def assert_screenshot(self, filename: str = '', test_name: str = '', name_suffix: str = '',
                          threshold: Union[int, float] = 0, delay: Union[int, float] = 0.5, scroll: bool = False,
                          remove: List[Any] = None) -> VisualComparison:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/netagative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :param remove: remove element from screenshot
        :return: self
        """
        if filename:
            if name_suffix:
                filename = f'{filename}_{name_suffix}'
        else:
            filename = self._get_screenshot_name(test_name, name_suffix)

        root_path = self.visual_regression_path

        if not root_path:
            raise Exception('Provide visual regression path to environment. '
                            f'Example: {self.__class__.__name__}.visual_regression_path = "src"')

        root_path = root_path if root_path.endswith('/') else f'{root_path}/'
        reference_directory = f'{root_path}reference/'
        output_directory = f'{root_path}output/'
        diff_directory = f'{root_path}difference/'

        reference_file = f'{reference_directory}{filename}.png'
        output_file = f'{output_directory}{filename}.png'
        diff_file = f'{diff_directory}/diff_{filename}.png'

        os.makedirs(os.path.dirname(reference_directory), exist_ok=True)
        os.makedirs(os.path.dirname(output_directory), exist_ok=True)
        os.makedirs(os.path.dirname(diff_directory), exist_ok=True)

        if scroll:
            self.element.scroll_into_view()

        time.sleep(delay)

        def save_screenshot(screenshot_name):
            self.element.get_screenshot(screenshot_name)
            if remove:
                self._remove_elements(self.element, remove, screenshot_name)

        try:
            Image.open(reference_file)
        except FileNotFoundError:
            save_screenshot(reference_file)

            if self.visual_reference_generation:
                return self

            raise FileNotFoundError(f'Reference file "{reference_file}" not found, but its just saved. '
                                    f'If it CI run, then you need to commit reference files.') from None

        save_screenshot(output_file)
        self._assert_same_images(output_file, reference_file, diff_file, threshold)
        return self

    def _assert_same_images(self, actual_file: str, reference_file: str, filename: str,
                            threshold: Union[int, float]) -> VisualComparison:
        """
        Assert that given images are equal to each other

        :param actual_file: actual image path
        :param reference_file: reference image path
        :param filename: difference image name
        :param threshold: possible difference in percents
        :return: VisualComparison
        """
        reference_image = Image.open(reference_file).convert('RGB')
        output_image = Image.open(actual_file).convert('RGB')
        diff, actual_threshold = self._get_difference(reference_image, output_image)

        same_size = reference_image.size == output_image.size
        is_different = actual_threshold > threshold

        if is_different or not same_size:
            diff.save(filename)
            self._attach_allure_diff(actual_file, reference_file, filename)

        base_error = f"The new screenshot '{actual_file}' did not match the reference '{reference_file}'."

        if not same_size:
            raise AssertionError(f'{base_error} Image size (width, height) is different: '
                                 f'Expected:{reference_image.size}, Actual: {output_image.size}.')
        if is_different:
            raise AssertionError(f"{base_error} Threshold is: {actual_threshold}; Possible threshold is: {threshold}")

        return self

    def _remove_elements(self, parent: Any, children: list, path: str) -> VisualComparison:
        """
        Remove elements from image

        :param parent: parent element
        :param children: list of children elements
        :param path: path to output file

        :return: self
        """
        parent_abs = {x: max(y, 0) for x, y in parent.get_rect().items()}

        for element in children:
            elem_rect = element.get_rect()

            if self.driver_wrapper.is_ios:
                elem_rect = {x: max(y, 0) for x, y in elem_rect.items()}

                if elem_rect['y'] != 0:
                    elem_rect['y'] += abs(self.driver_wrapper.get_top_bar_height())

            zone = {item: int(elem_rect[item] - (parent_abs[item] if item in ['x', 'y'] else 0)) for item in elem_rect}
            remove_coordinates = (zone['x'], zone['y'], zone['x'] + zone['width'], zone['y'] + zone['height'])
            image = Image.open(path).convert('RGB')
            image.paste("#000000", remove_coordinates)
            image.save(path)

        return self

    def _get_screenshot_name(self, test_function_name: str = '', name_suffix: str = '') -> str:
        """
        Get screenshot name

        :param test_function_name: execution test name. Will try to find it automatically if empty string given
        :return: custom screenshot filename:
          :::
          - playwright: test_screenshot_rubiks_cube_playwright_chromium
          - selenium: test_screenshot_rubiks_cube_mac_os_x_selenium_chrome
          - appium ios: test_screenshot_rubiks_cube_iphone_13_v_15_4_appium_safari
          - appium android: test_screenshot_rubiks_cube_pixel5_v_12_appium_chrome
          :::
        """
        if not test_function_name:
            back_frame = get_frame().f_back
            test_function_name = ''
            try:
                for _ in range(50):
                    if 'test' not in test_function_name or 'test' not in back_frame.f_code.co_filename:
                        back_frame = back_frame.f_back
                        test_function_name = back_frame.f_code.co_name
                    else:
                        break
            except AttributeError:
                raise Exception("Can't find test name. Please pass the test_name as parameter to assert_screenshot")
        else:
            test_function_name = test_function_name.replace('[', '_')

        if self.driver_wrapper.mobile:
            caps = self.driver_wrapper.driver.caps

            device_name = caps.get('customDeviceName', '')

            if self.driver_wrapper.is_android and not device_name:
                device_name = caps.get('avd', f'{caps.get("deviceManufacturer")}_{caps.get("deviceModel", "none")}')
            elif self.driver_wrapper.is_ios and not device_name:
                device_name = caps['deviceName']

            browser_name = caps['browserName']
            platform_version = caps['platformVersion']
            screenshot_name = f'{device_name}_v_{platform_version}_appium_{browser_name}'
        elif self.driver_wrapper.selenium:
            caps = self.driver_wrapper.driver.caps
            platform_name, browser_name = caps["platformName"], caps['browserName']
            screenshot_name = f'{platform_name}_selenium_{browser_name}'
        elif self.driver_wrapper.playwright:
            caps = self.driver_wrapper.instance
            screenshot_name = f'playwright_{caps.browser_type.name}'
        else:
            raise DriverWrapperException('Cant find current platform')

        name_suffix = f'_{name_suffix}_' if name_suffix else '_'

        screenshot_name = f'{test_function_name}_{self.element.name}{name_suffix}{screenshot_name}'

        for item in (']', '"', "'"):
            screenshot_name = screenshot_name.replace(item, '')

        for item in punctuation + ' ':
            screenshot_name = screenshot_name.replace(item, '_')

        return screenshot_name.lower()

    @staticmethod
    def _get_difference(im1: Image, im2: Image):
        """
        Calculate difference between two images

        :param im1: image 1
        :param im2: image 2
        :return: (diff image, diff float value )
        """
        diff = ImageChops.difference(im1, im2)
        histogram = diff.histogram()

        rms = reduce(
            operator.add,
            map(
                lambda h, i: h * (i ** 2),
                histogram,
                range(256)
            )
        )

        return diff, math.sqrt(rms / (float(im1.size[0]) * im1.size[1]))

    @staticmethod
    def _attach_allure_diff(actual_path: str, expected_path: str, diff_path: str) -> None:
        """
        Attach screenshots to allure screen diff plugin
        https://github.com/allure-framework/allure2/blob/master/plugins/screen-diff-plugin/README.md

        :param actual_path: path of actual image
        :param expected_path: path of expected image
        :param diff_path: path of diff image
        :return: None
        """
        allure = None

        try:
            allure = importlib.import_module('allure')
        except ModuleNotFoundError:
            autolog('Skip screenshot attaching due to allure module not found')

        if allure:

            diff_dict = {}
            for name, path in (('actual', actual_path), ('expected', expected_path), ('diff', diff_path)):
                image = open(path, 'rb')
                diff_dict.update({name: f'data:image/png;base64,{base64.b64encode(image.read()).decode("ascii")}'})
                image.close()

            allure.attach(name='diff', body=json.dumps(diff_dict), attachment_type='application/vnd.allure.image.diff')
