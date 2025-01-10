import inspect
from unittest.mock import MagicMock

import pytest

from mops.visual_comparison import VisualComparison


def default_parameters(func):
    return [None for _ in range(len(inspect.signature(func).parameters) - 1)]


@pytest.fixture
def enable_skip():
    default_value = VisualComparison.skip_screenshot_comparison
    VisualComparison.skip_screenshot_comparison = True
    yield
    VisualComparison.skip_screenshot_comparison = default_value


def test_skip_visual_comparison(enable_skip):
    params = default_parameters(VisualComparison.assert_screenshot)
    instance = VisualComparison(None, None)

    instance._get_screenshot_name = MagicMock(return_value='test_screenshot')
    instance._save_screenshot = MagicMock()
    instance._assert_same_images = MagicMock()

    instance.assert_screenshot(*params)
    instance._get_screenshot_name.assert_not_called()
    instance._save_screenshot.assert_not_called()
    instance._assert_same_images.assert_not_called()
