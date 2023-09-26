import os

import pytest
import pytest_rerunfailures


@pytest.mark.parametrize('with_name', [True, False], ids=['screenshot name given', 'screenshot name missed'])
def test_screenshot(base_playground_page, driver_name, platform, with_name):
    filename = f'{driver_name}-{platform}-kube' if with_name else ''
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename)


@pytest.mark.parametrize('with_name', [True, False], ids=['screenshot name given', 'screenshot name missed'])
def test_screenshot_name_with_suffix(base_playground_page, driver_name, platform, with_name):
    filename = f'{driver_name}-{platform}-kube' if with_name else ''
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename, name_suffix='first')
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename, name_suffix='second')


def test_screenshot_remove(base_playground_page):
    base_playground_page.text_container.scroll_into_view(sleep=0.5).assert_screenshot(
            remove=[base_playground_page.inner_text_1, base_playground_page.inner_text_2])


@pytest.fixture
def file(request):
    request.node.execution_count = 1
    request.node.session.config.option.reruns = 1
    filename = 'reference_with_rerun'
    yield filename
    request.node.session.config.option.reruns = 0
    if not request.config.option.sv:
        os.remove(f'{os.getcwd()}/tests/adata/visual/reference/{filename}.png')


def test_screenshot_without_reference_and_rerun(base_playground_page, file, request):
    assert pytest_rerunfailures.get_reruns_count(request.node) == 1
    try:
        base_playground_page.text_container.scroll_into_view(sleep=0.5).assert_screenshot(filename=file)
    except AssertionError:
        pass
    else:
        options = request.config.option
        if not any([options.gr, options.hgr, options.sv, options.sgr]):
            raise Exception('Unexpected behavior')


def test_screenshot_fill_background_default(base_playground_page):
    base_playground_page.kube.scroll_into_view().assert_screenshot(fill_background=True)


def test_screenshot_fill_background_blue(base_playground_page):
    base_playground_page.kube.scroll_into_view().assert_screenshot(fill_background='blue')
