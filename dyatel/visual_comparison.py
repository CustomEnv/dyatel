import importlib
import json
import base64
import math
import operator
import os
from functools import reduce
from typing import Union

from PIL import Image, ImageChops

from dyatel.mixins.log_mixin import autolog


def assert_same_images(actual_file: str, reference_file: str, filename: str, threshold: Union[int, float]) -> None:
    """
    Assert that given images are equal to each other

    :param actual_file: actual image path
    :param reference_file: reference image path
    :param filename: difference image name
    :param threshold: possible difference in percents
    :return: None
    """
    reference_image = Image.open(reference_file).convert('RGB')
    output_image = Image.open(actual_file).convert('RGB')
    diff, actual_threshold = get_difference(reference_image, output_image)

    same_size = reference_image.size == output_image.size
    is_different = actual_threshold > threshold

    if is_different or not same_size:
        root_path = os.environ.get('visual', '')
        diff_directory = f'{root_path}/difference/'
        os.makedirs(os.path.dirname(diff_directory), exist_ok=True)
        diff_file = f'{diff_directory}/diff-{filename}.png'
        diff.save(diff_file)
        attach_allure_diff(actual_file, reference_file, diff_file)

    base_error = f"The new screenshot '{actual_file}' did not match the reference '{reference_file}'."

    if not same_size:
        raise AssertionError(f'{base_error} Image size (width, height) is different: '
                             f'Expected:{reference_image.size}, Actual: {output_image.size}.')
    if is_different:
        raise AssertionError(f"{base_error} Threshold is: {actual_threshold}; Possible threshold is: {threshold}")


def get_difference(im1: Image, im2: Image):
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


def attach_allure_diff(actual_path: str, expected_path: str, diff_path: str) -> None:
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
