import os

import pytest
import pytest_rerunfailures
from dyatel.visual_comparison import VisualComparison


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


def test_screenshot_soft_assert(base_playground_page):
    base_playground_page.kube.scroll_into_view().soft_assert_screenshot(
        test_name=test_screenshot_fill_background_default.__name__
    )


def test_screenshot_fill_background_blue(base_playground_page):
    base_playground_page.kube.scroll_into_view().assert_screenshot(fill_background='blue')


def test_screenshot_fill_background_default(base_playground_page):
    base_playground_page.kube.scroll_into_view().assert_screenshot(fill_background=True)


def test_assert_screenshot_hide_elements(second_playground_page, driver_wrapper):
    all_cards = second_playground_page.get_all_cards()
    for card in all_cards:
        print(card.element)
    second_playground_page.row_with_cards.assert_screenshot(
        hide=all_cards[1],
        name_suffix='middle hidden'
    )
    driver_wrapper.refresh()
    second_playground_page.row_with_cards.scroll_into_view()
    all_cards = second_playground_page.get_all_cards()
    second_playground_page.row_with_cards.assert_screenshot(
        hide=[all_cards[0], all_cards[2]],
        name_suffix='sides hidden'
    )


def test_assert_screenshot_hide_driver_elements(second_playground_page, driver_wrapper):
    all_cards = second_playground_page.get_all_cards()
    second_playground_page.row_with_cards.scroll_into_view()
    driver_wrapper.assert_screenshot(
        hide=all_cards[1],
        name_suffix='middle hidden'
    )
    driver_wrapper.refresh()
    second_playground_page.row_with_cards.scroll_into_view()
    all_cards = second_playground_page.get_all_cards()
    driver_wrapper.assert_screenshot(
        hide=[all_cards[0], all_cards[2]],
        name_suffix='sides hidden'
    )


def test_assert_screenshot_negative_different_sizes(second_playground_page, driver_wrapper):
    first_card = second_playground_page.get_all_cards()[0]
    vc = VisualComparison(driver_wrapper, element=first_card)
    filename = vc._get_screenshot_name()
    vc._save_screenshot(
        screenshot_name=f'tests/adata/visual/reference/{filename}.png',
        delay=1,
        remove=[],
        fill_background=False,
    )
    driver_wrapper.execute_script('arguments[0].style = "width: 600px"', first_card.element)
    try:
        first_card.scroll_into_view().assert_screenshot()
    except AssertionError as exc:
        assert f"Image size (width, height) is not same for '{filename}'" in str(exc)
    else:
        raise Exception('Unexpected behavior')


def test_assert_screenshot_negative_missmatch(second_playground_page, driver_wrapper):
    first_card = second_playground_page.get_all_cards()[0]
    vc = VisualComparison(driver_wrapper, element=first_card)
    filename = vc._get_screenshot_name()
    vc._save_screenshot(
        screenshot_name=f'tests/adata/visual/reference/{filename}.png',
        delay=1,
        remove=[],
        fill_background=False,
    )
    try:
        first_card.scroll_into_view().assert_screenshot(fill_background=True)
    except AssertionError as exc:
        assert f"Visual mismatch found for '{filename}'" in str(exc)
    else:
        raise Exception('Unexpected behavior')
