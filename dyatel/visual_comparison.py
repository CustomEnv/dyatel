from __future__ import annotations

import os
import re
import time
import math
import json
import base64
import importlib
from urllib.parse import urljoin
from typing import Union, List, Any, Tuple, Optional
from string import punctuation

try:
    import cv2.cv2 as cv2  # ~cv2@4.5.5.62 + python@3.8/9/10
except ImportError:
    import cv2  # ~cv2@4.10.0.84 + python@3.11/12
import numpy
from skimage._shared.utils import check_shape_equality  # noqa
from skimage.metrics import structural_similarity
from PIL import Image

from dyatel.exceptions import DriverWrapperException, TimeoutException
from dyatel.js_scripts import add_element_over_js, delete_element_over_js
from dyatel.mixins.objects.cut_box import CutBox
from dyatel.utils.logs import autolog
from dyatel.mixins.internal_mixin import get_element_info


class VisualComparison:

    visual_regression_path = ''
    test_item = None
    attach_diff_image_path = False
    skip_screenshot_comparison = False
    visual_reference_generation = False
    hard_visual_reference_generation = False
    soft_visual_reference_generation = False
    default_delay = 0.75
    default_threshold = 0
    dynamic_threshold_factor = 0
    diff_color_scheme = (0, 255, 0)

    __initialized = False

    def __init__(self, driver_wrapper, element=None):
        self.driver_wrapper = driver_wrapper
        self.dyatel_element = element
        self.screenshot_name = 'default'

        if self.dynamic_threshold_factor and self.default_threshold:
            raise Exception('Provide only one argument for threshold of visual comparison')

        if not self.__initialized:
            self.__init_session()

    def __init_session(self):
        root_path = self.visual_regression_path

        if not root_path:
            raise Exception('Provide visual regression path to environment. '
                            f'Example: {self.__class__.__name__}.visual_regression_path = "src"')

        root_path = root_path if root_path.endswith('/') else f'{root_path}/'
        self.reference_directory = f'{root_path}reference/'
        self.output_directory = f'{root_path}output/'
        self.diff_directory = f'{root_path}difference/'

        os.makedirs(os.path.dirname(self.reference_directory), exist_ok=True)
        os.makedirs(os.path.dirname(self.output_directory), exist_ok=True)
        os.makedirs(os.path.dirname(self.diff_directory), exist_ok=True)

        self.__initialized = True

    def _save_screenshot(
            self,
            screenshot_name: str,
            delay: Union[int, float],
            remove: list,
            fill_background: bool,
            cut_box: Optional[CutBox],
    ):
        time.sleep(delay)

        self._fill_background(fill_background)
        self._appends_dummy_elements(remove)

        desired_obj = self.dyatel_element or self.driver_wrapper.anchor or self.driver_wrapper
        image = desired_obj.screenshot_image()

        if cut_box:
            image = image.crop(cut_box.get_box(image.size))

        desired_obj.save_screenshot(screenshot_name, screenshot_base=image)

        self._remove_dummy_elements()

    def assert_screenshot(
            self,
            filename: str,
            test_name: str,
            name_suffix: str,
            threshold: Union[int, float],
            delay: Union[int, float],
            scroll: bool,
            remove: List[Any],
            fill_background: Union[str, bool],
            cut_box: Optional[CutBox]
    ) -> VisualComparison:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/negative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :param remove: remove elements from screenshot
        :param fill_background: fill background with given color or black color by default
        :param cut_box: custom coordinates, that will be cut from original image (left, top, right, bottom)
        :return: self
        """
        remove = remove if remove else []
        screenshot_params = dict(delay=delay, remove=remove, fill_background=fill_background, cut_box=cut_box)

        if self.skip_screenshot_comparison:
            return self

        if filename:
            if name_suffix:
                filename = f'{filename}_{name_suffix}'
            self.screenshot_name = filename
        else:
            self.screenshot_name = self._get_screenshot_name(test_name, name_suffix)

        reference_file = f'{self.reference_directory}{self.screenshot_name}.png'
        output_file = f'{self.output_directory}{self.screenshot_name}.png'
        diff_file = f'{self.diff_directory}diff_{self.screenshot_name}.png'

        if scroll:
            self.dyatel_element.scroll_into_view()

        if self.hard_visual_reference_generation:
            self._save_screenshot(reference_file, **screenshot_params)
            return self

        image = cv2.imread(reference_file)
        if isinstance(image, type(None)):
            self._save_screenshot(reference_file, **screenshot_params)

            if self.visual_reference_generation or self.soft_visual_reference_generation:
                return self

            self._disable_reruns()

            self._attach_allure_diff(reference_file, reference_file, reference_file)
            raise AssertionError(f'Reference file "{reference_file}" not found, but its just saved. '
                                 f'If it CI run, then you need to commit reference files.')

        if self.visual_reference_generation and not self.soft_visual_reference_generation:
            return self

        self._save_screenshot(output_file, **screenshot_params)

        try:
            self._assert_same_images(output_file, reference_file, diff_file, threshold)
        except AssertionError as exc:
            if self.soft_visual_reference_generation:
                self._save_screenshot(reference_file, **screenshot_params)
            else:
                raise exc

        return self

    @staticmethod
    def calculate_threshold(file: str, dynamic_threshold_factor: int = None) -> Tuple:
        """
        Calculate possible threshold, based on dynamic_threshold_factor

        :param file: image file path for calculation
        :param dynamic_threshold_factor: use provided threshold factor
        :return: tuple of calculated threshold and additional data
        """
        factor = VisualComparison.dynamic_threshold_factor or dynamic_threshold_factor
        img = Image.open(file)
        width, height = img.size
        pixels_grid = height * width
        calculated_threshold = factor / math.sqrt(pixels_grid)
        pixels_allowed = int(pixels_grid / 100 * calculated_threshold)
        return calculated_threshold, \
            f'\nAdditional info: {width}x{height}; {calculated_threshold=}; {pixels_allowed=} from {pixels_grid}'

    def _appends_dummy_elements(self, remove_data: list) -> VisualComparison:
        """
        Placed an element above each from given list and paints it black

        :param remove_data: list of elements to be fake removed
        :return: VisualComparison
        """
        for obj in remove_data:

            try:
                obj.wait_visibility()
            except TimeoutException:
                msg = f'Cannot find {obj.name} while removing background from screenshot. {get_element_info(obj)}'
                raise TimeoutException(msg)

            self.driver_wrapper.execute_script(add_element_over_js, obj)
        return self

    def _remove_dummy_elements(self) -> VisualComparison:
        """
        Remove all dummy elements from DOM

        :return: VisualComparison
        """
        self.driver_wrapper.execute_script(delete_element_over_js)
        return self

    def _fill_background(self, fill_background_data) -> VisualComparison:
        """
        Fill background of element

        :param fill_background_data: fill background with given color or black color by default
        :return: VisualComparison
        """
        if not fill_background_data:
            return self

        dyatel_element = self.dyatel_element

        if fill_background_data is True:
            dyatel_element.execute_script('arguments[0].style.background = "#000";')
        elif type(fill_background_data) is str:
            dyatel_element.execute_script(f'arguments[0].style.background = "{fill_background_data}";')

        return self

    def _assert_same_images(self, actual_file: str, reference_file: str, diff_file: str,
                            threshold: Union[int, float]) -> VisualComparison:
        """
        Assert that given images are equal to each other

        :param actual_file: actual image path
        :param reference_file: reference image path
        :param diff_file: difference image name
        :param threshold: possible difference in percents
        :return: VisualComparison
        """
        reference_image = cv2.imread(reference_file)
        output_image = cv2.imread(actual_file)
        threshold = threshold if threshold else self.default_threshold

        additional_data = ''
        if not threshold:
            threshold, additional_data = self.calculate_threshold(reference_file)

        try:
            check_shape_equality(reference_image, output_image)
        except ValueError:
            self._attach_allure_diff(actual_file, reference_file, actual_file)
            # todo: watermark / fill size difference with color on diff image is better, but need more time
            # rescale output image to the size of reference image, and save it as diff image
            height, width, _ = reference_image.shape
            scaled_image = cv2.resize(output_image, (width, height))
            cv2.imwrite(diff_file, scaled_image)
            raise AssertionError(f"↓\nImage size (width, height) is not same for '{self.screenshot_name}':"
                                 f"\nExpected: {reference_image.shape[0:2]};"
                                 f"\nActual: {output_image.shape[0:2]}.")

        diff, actual_threshold = self._get_difference(reference_image, output_image, threshold)
        is_different = actual_threshold > threshold

        if is_different:
            cv2.imwrite(diff_file, diff)
            self._attach_allure_diff(actual_file, reference_file, diff_file)

        diff_data = ""
        if self.attach_diff_image_path:
            diff_data = f"\nDiff image {urljoin('file:', diff_file)}"

        base_error = f"↓\nVisual mismatch found for '{self.screenshot_name}'{diff_data}"

        if is_different:
            raise AssertionError(f"{base_error}:"
                                 f"\nThreshold is: {actual_threshold};"
                                 f"\nPossible threshold is: {threshold}"
                                 + additional_data)

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
        test_function_name = test_function_name if test_function_name else getattr(self.test_item, 'name', '')
        if not test_function_name:
            raise Exception('Draft: provide test item self.test_item')

        test_function_name = test_function_name.replace('[', '_')  # required here for better separation

        if self.driver_wrapper.is_android or self.driver_wrapper.is_ios:
            caps = self.driver_wrapper.driver.caps
            device_name = caps.get('customDeviceName', '')

            if self.driver_wrapper.is_android and not device_name:
                device_name = caps.get('avd', f'{caps.get("deviceManufacturer")}_{caps.get("deviceModel", "none")}')
            elif self.driver_wrapper.is_ios and not device_name:
                device_name = caps['deviceName']

            platform_version = caps['platformVersion']
            screenshot_name = f'{device_name}_v_{platform_version}_appium_{self.driver_wrapper.browser_name}'
        elif self.driver_wrapper.is_selenium:
            platform_name = self.driver_wrapper.driver.caps["platformName"]
            screenshot_name = f'{platform_name}_selenium_{self.driver_wrapper.browser_name}'
        elif self.driver_wrapper.is_playwright:
            screenshot_name = f'playwright_{self.driver_wrapper.browser_name}'
        else:
            raise DriverWrapperException('Cant find current platform')

        name_suffix = f'_{name_suffix}_' if name_suffix else '_'
        location_name = self.dyatel_element.name if self.dyatel_element else 'entire_screen'
        base_name = f'{test_function_name}{location_name}{name_suffix}'
        if 'mobile' not in base_name and self.driver_wrapper.is_mobile_resolution:
            location_name += '_mobile_'
        screenshot_name = f'{test_function_name}_{location_name}{name_suffix}{screenshot_name}'

        for item in (']', '"', "'"):
            screenshot_name = screenshot_name.replace(item, '')

        for item in punctuation + ' ':
            screenshot_name = screenshot_name.replace(item, '_')

        return self._remove_unexpected_underscores(screenshot_name).lower()

    def _get_difference(
            self,
            reference_img: numpy.ndarray,
            actual_img: numpy.ndarray,
            possible_threshold: Union[int, float]
    ) -> tuple[numpy.ndarray, float]:
        """
        Calculate difference between two images

        :param reference_img: image 1, numpy.ndarray
        :param actual_img: image 2, numpy.ndarray
        :return: (diff image, diff float value )
        """
        # Convert images to grayscale
        reference_img_gray = cv2.cvtColor(reference_img, cv2.COLOR_BGR2GRAY)
        actual_img_gray = cv2.cvtColor(actual_img, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between the two images
        score, diff = structural_similarity(reference_img_gray, actual_img_gray, full=True)
        score *= 100

        # The diff image contains the actual image differences between the two images
        # and is represented as a floating point data type in the range [0,1]
        # so we must convert the array to 8-bit unsigned integers in the range
        # [0,255] before we can use it with OpenCV
        diff = (diff * 255).astype("uint8")
        diff_box = cv2.merge([diff, diff, diff])

        # Threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = numpy.zeros(reference_img.shape, dtype='uint8')
        filled_after = actual_img.copy()
        percent_diff = 100 - score
        is_different_enough = percent_diff > possible_threshold

        for c in contours:
            if is_different_enough or cv2.contourArea(c) > 40:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(reference_img, (x, y), (x + w, y + h), self.diff_color_scheme, 2)
                cv2.rectangle(actual_img, (x, y), (x + w, y + h), self.diff_color_scheme, 2)
                cv2.rectangle(diff_box, (x, y), (x + w, y + h), self.diff_color_scheme, 2)
                cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
                cv2.drawContours(filled_after, [c], 0, self.diff_color_scheme, -1)

        diff_image, percent_diff = filled_after, 100 - score
        return diff_image, percent_diff

    def _attach_allure_diff(self, actual_path: str, expected_path: str, diff_path: str = None) -> None:
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
            data = [('actual', actual_path), ('expected', expected_path)]
            diff_dict = {}

            if diff_path:
                data.append(('diff', diff_path))

            for name, path in data:
                with open(path, 'rb') as image:
                    diff_dict.update({name: f'data:image/png;base64,{base64.b64encode(image.read()).decode("ascii")}'})

            allure.attach(
                name=f'diff_for_{self.screenshot_name}',
                body=json.dumps(diff_dict),
                attachment_type='application/vnd.allure.image.diff'
            )

    def _disable_reruns(self) -> None:
        """
        Disable reruns for pytest

        :return: None
        """
        try:
            pytest_rerun = importlib.import_module('pytest_rerunfailures')
        except ModuleNotFoundError:
            return None

        if hasattr(self.test_item, 'execution_count'):
            self.test_item.execution_count = pytest_rerun.get_reruns_count(self.test_item) + 1

    @staticmethod
    def _remove_unexpected_underscores(text) -> str:
        """
        Remove multiple underscores from given text

        :return: test_screenshot__data___name -> test_screenshot_data_name
        """
        return re.sub(r'_{2,}', '_', text)
