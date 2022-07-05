import math
import operator
import os
from functools import reduce

from PIL import Image, ImageChops


def assert_same_images(actual_file, reference_file, filename, threshold):
    reference_image = Image.open(reference_file).convert('RGB')
    output_image = Image.open(actual_file).convert('RGB')
    diff, actual_threshold = get_difference(reference_image, output_image)
    if actual_threshold > threshold:
        root_path = os.environ.get('visual', '')
        diff_file = f'{root_path}/difference/diff-{filename}.png'
        diff.save(diff_file)
        raise AssertionError(f"The new screenshot '{actual_file}' did not match the"
                             f" reference '{reference_file}'. Threshold is: {actual_threshold}")


def get_difference(im1, im2):
    diff = ImageChops.difference(im1, im2)
    histogram = diff.histogram()

    red = reduce(
            operator.add,
            map(
                lambda h, i: h * (i ** 2),
                histogram,
                range(256)
            )
        )

    return diff, math.sqrt(red / (float(im1.size[0]) * im1.size[1]))

