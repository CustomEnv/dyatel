import inspect
import time

import pytest

from dyatel.visual_comparison import VisualComparison


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
    start = time.time()
    VisualComparison(None, None).assert_screenshot(*params)
    end = time.time() - start
    assert end < 0.001
