import random
import time

import pytest

from dyatel.exceptions import UnexpectedElementsCountException, NoSuchElementException
from dyatel.mixins.element_mixin import ElementMixin
from tests.adata.pages.keyboard_page import KeyboardPage


@pytest.mark.skip_platform(
    'playwright',
    reason='Playwright doesnt throw error if element/parent isn\'t available/broken'
)
def test_element_exception_without_parent(base_playground_page):
    el = base_playground_page.kube_broken
    try:
        el._get_element(wait=False)
    except NoSuchElementException as exc:
        logs = ElementMixin().get_element_logging_data(el)
        message = f'Cant find element "{el.name}". {logs}'
        assert exc.msg == message


@pytest.mark.skip_platform(
    'playwright',
    reason='Playwright doesnt throw error if element/parent isn\'t available/broken'
)
def test_element_exception_with_broken_parent(base_playground_page):
    el = base_playground_page.kube_broken_parent
    try:
        el._get_element(wait=False)
    except NoSuchElementException as exc:
        logs = ElementMixin().get_element_logging_data(el.parent)
        message = f'Cant find parent element "{el.parent.name}". {logs}'
        assert exc.msg == message


def test_element_displayed_positive(base_playground_page):
    assert base_playground_page.kube.is_displayed()


def test_element_displayed_negative(base_playground_page):
    assert not base_playground_page.kube_broken.is_displayed()


def test_all_elements_count_positive(base_playground_page):
    assert base_playground_page.any_link.get_elements_count() > 1


def test_all_elements_count_negative(base_playground_page):
    assert base_playground_page.kube_broken.get_elements_count() == 0


@pytest.mark.xfail_platform('android', 'ios', reason='Can not get text from that element. TODO: Rework test')
def test_type_clear_text_get_value(pizza_order_page):
    text_to_send = str(random.randint(100, 9999))
    pizza_order_page.quantity_input.type_text(text_to_send)
    text_added = pizza_order_page.quantity_input.value == text_to_send
    pizza_order_page.quantity_input.clear_text()
    text_erased = pizza_order_page.quantity_input.value == ''
    assert all((text_added, text_erased))


def test_hover(mouse_event_page):
    initial_not_displayed = not mouse_event_page.dropdown.is_displayed()
    mouse_event_page.choose_language_button.scroll_into_view(sleep=0.1).hover()
    after_hover_displayed = mouse_event_page.dropdown.wait_element_without_error().is_displayed()
    mouse_event_page.choose_language_button.hover_outside()
    after_outside_hover_displayed = not mouse_event_page.dropdown.wait_element_hidden().is_displayed()
    assert all((initial_not_displayed, after_hover_displayed, after_outside_hover_displayed))


@pytest.mark.parametrize('with_name', [True, False], ids=['screenshot name given', 'screenshot name missed'])
def test_screenshot(base_playground_page, driver_engine, driver_name, platform, with_name):
    filename = f'{driver_engine}-{driver_name}-{platform}-kube' if with_name else ''
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename, threshold=6)


@pytest.mark.parametrize('with_name', [True, False], ids=['screenshot name given', 'screenshot name missed'])
def test_screenshot_name_with_suffix(base_playground_page, driver_engine, driver_name, platform, with_name):
    filename = f'{driver_engine}-{driver_name}-{platform}-kube' if with_name else ''
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename, name_suffix='first', threshold=6)
    base_playground_page.kube.scroll_into_view().assert_screenshot(filename, name_suffix='second', threshold=6)


def test_screenshot_remove(base_playground_page):
    base_playground_page.text_container.scroll_into_view(sleep=0.5).assert_screenshot(
            remove=[base_playground_page.inner_text_1, base_playground_page.inner_text_2])

# Test waits


def test_wait_without_error(pizza_order_page):
    pizza_order_page.error_modal.wait_element_without_error(timeout=0.01)
    assert not pizza_order_page.error_modal.is_displayed()


def test_click_and_wait(pizza_order_page, driver_engine):
    pizza_order_page.submit_button.click()
    after_click_displayed = pizza_order_page.error_modal.wait_element().is_displayed()
    if 'play' in driver_engine:
        time.sleep(1)
    pizza_order_page.error_modal.click_outside()
    after_click_outside_not_displayed = not pizza_order_page.error_modal.wait_element_hidden().is_displayed()
    assert all((after_click_displayed, after_click_outside_not_displayed))


def test_click_into_center(mouse_event_page, platform):
    mouse_event_page.mouse_click_card().click_area.click_into_center()
    result_x, result_y = mouse_event_page.mouse_click_card().get_result_coordinates()
    expected_x_range, expected_y_range = mouse_event_page.mouse_click_card().get_click_area_middle()
    assert result_x in expected_x_range, f'result_x: {result_x}; expected_x: {expected_x_range}'
    assert result_y in expected_y_range, f'result_y: {result_y}; expected_y: {expected_y_range}'


@pytest.mark.parametrize('coordinates', [(-2, -2), (2, 2), (2, -2), (-2, 2), (2, 0), (0, 2)])
def test_click_outside(mouse_event_page, platform, coordinates):
    mouse_event_page.mouse_click_card().click_area_parent.click_outside(*coordinates)
    assert not mouse_event_page.mouse_click_card().is_click_proceeded()


@pytest.mark.xfail_platform('android', 'ios', reason='Can not get value from that element. TODO: Rework test')
def test_wait_element_value(expected_condition_page):
    expected_condition_page.value_card.trigger_button.click()
    value_without_wait = expected_condition_page.value_card.wait_for_value_input.value
    expected_condition_page.value_card.wait_for_value_input.wait_element_value()
    value_with_wait = expected_condition_page.value_card.wait_for_value_input.value == 'Dennis Ritchie'
    assert all((not value_without_wait, value_with_wait))


@pytest.mark.xfail_platform('playwright', 'safari', reason='Unexpected text')
def test_wait_element_text(expected_condition_page):
    expected_condition_page.value_card.trigger_button.click()
    value_without_wait = expected_condition_page.value_card.wait_for_text_button.text
    expected_condition_page.value_card.wait_for_text_button.wait_element_text()
    value_with_wait = expected_condition_page.value_card.wait_for_text_button.text == 'Submit'
    assert all((not value_without_wait, value_with_wait))


def test_wait_elements_count(forms_page):
    forms_page.validation_form.form_mixin.input.type_text('sample')
    forms_page.validation_form.submit_form_button.click()
    forms_page.validation_form.any_error.wait_elements_count(4)
    assert forms_page.validation_form.any_error.get_elements_count() == 4


def test_wait_elements_count_v2(expected_condition_page):
    initial_count = expected_condition_page.frame_card.frame.get_elements_count()
    expected_condition_page.frame_card.trigger_button.click()
    target_count = expected_condition_page.frame_card.frame.wait_elements_count(1).get_elements_count()
    assert all((initial_count == 0, target_count == 1))


def test_wait_elements_count_negative(forms_page):
    forms_page.validation_form.form_mixin.input.type_text('sample')
    forms_page.validation_form.submit_form_button.click()

    try:
        forms_page.validation_form.any_error.wait_elements_count(3, timeout=1)
    except UnexpectedElementsCountException:
        pass
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.xfail(reason='TODO: Implementation')
def test_wait_element_stop_changing(progressbar_page):
    # bar = progressbar_page.progress_bar.element
    # progressbar_page.start_button.click()
    # locations_list = [tuple(bar.size.values()) for _ in range(200) if not time.sleep(0.1)]
    pass


@pytest.mark.xfail(reason='TODO: Implementation')
def test_wait_element_stop_moving(progressbar_page):
    # bar = progressbar_page.progress_bar.element
    # progressbar_page.start_button.click()
    # locations_list = [tuple(bar.location.values()) for _ in range(200) if not time.sleep(0.1)]
    pass


# Cases when parent is another element


def test_parent_element_positive(base_playground_page):
    assert base_playground_page.kube_parent.is_displayed()


def test_parent_element_negative(base_playground_page):
    assert not base_playground_page.kube_wrong_parent.is_displayed()


def test_parent_element_wait_visible_positive(base_playground_page):
    assert base_playground_page.kube_parent.wait_element()


def test_parent_element_wait_hidden_negative(base_playground_page):
    assert base_playground_page.kube_wrong_parent.wait_element_hidden()


# Other cases with parent


def test_all_elements_with_parent(base_playground_page):
    """ all_elements when parent of Element is Page """
    all_elements = base_playground_page.any_div_with_parent.all_elements
    assert all_elements, 'did not find elements on page'

    for element in all_elements:
        assert element.parent == base_playground_page


def test_element_group_all_elements_child(second_playground_page):
    """ all_elements when parent of Element is Group """
    all_cards = second_playground_page.get_all_cards()

    for index, element_object in enumerate(all_cards):
        if 0 < index < len(all_cards) - 1:
            assert element_object.button.element != all_cards[index - 1].button.element
            assert element_object.button.element != all_cards[index + 1].button.element

    all_cards[1].button.click()
    assert KeyboardPage().wait_page_loaded().is_page_opened()
