import random
import time

import pytest
from selenium.common.exceptions import NoSuchElementException

from dyatel.internal_utils import Mixin
from tests.adata.pages.mouse_event_page import MouseEventPage


@pytest.mark.skip_platform(
    'playwright',
    reason='Playwright doesnt throw error if element/parent isn\'t available/broken'
)
def test_element_exception_without_parent_form_driver(base_playground_page):
    el = base_playground_page.kube_broken
    try:
        el._get_element(wait=False)
    except NoSuchElementException as exc:
        logs = Mixin().get_element_logging_data(el)
        message = f'Cant find element "{el.name}". {logs}.'
        assert exc.msg == message


@pytest.mark.skip_platform(
    'playwright',
    reason='Playwright doesnt throw error if element/parent isn\'t available/broken'
)
def test_element_exception_with_broken_parent_form_driver(base_playground_page):
    el = base_playground_page.kube_broken_parent
    try:
        el._get_element(wait=False)
    except NoSuchElementException as exc:
        logs = Mixin().get_element_logging_data(el.parent)
        message = f'Cant find parent element "{el.parent.name}". {logs}.'
        assert exc.msg == message


def test_element_displayed_positive(base_playground_page):
    assert base_playground_page.kube.is_displayed()


def test_element_displayed_negative(base_playground_page):
    assert not base_playground_page.kube_broken.is_displayed()


def test_all_elements(base_playground_page):
    assert len(base_playground_page.any_link.all_elements) > 1


def test_all_elements_count(base_playground_page):
    assert base_playground_page.any_link.get_elements_count() > 1


def test_click_and_wait(pizza_order_page, driver_engine):
    pizza_order_page.submit_button.click()
    after_click_displayed = pizza_order_page.error_modal.wait_element().is_displayed()
    if 'play' in driver_engine:
        time.sleep(1)
    pizza_order_page.error_modal.click_outside()
    after_click_outside_not_displayed = not pizza_order_page.error_modal.wait_element_hidden().is_displayed()
    assert all((after_click_displayed, after_click_outside_not_displayed))


def test_wait_without_error(pizza_order_page):
    pizza_order_page.error_modal.wait_element_without_error(timeout=0.01)
    assert not pizza_order_page.error_modal.is_displayed()


@pytest.mark.xfail_platform('android', 'ios', reason='Can not get text from that element. TODO: Rework test')
def test_type_clear_text_get_value(pizza_order_page):
    text_to_send = str(random.randint(100, 9999))
    pizza_order_page.quantity_input.type_text(text_to_send)
    text_added = pizza_order_page.quantity_input.get_value == text_to_send
    pizza_order_page.quantity_input.clear_text()
    text_erased = pizza_order_page.quantity_input.get_value == ''
    assert all((text_added, text_erased))


def test_hover(mouse_event_page):
    initial_not_displayed = not mouse_event_page.dropdown.is_displayed()
    mouse_event_page.choose_language_button.scroll_into_view(sleep=0.1).hover()
    after_hover_displayed = mouse_event_page.dropdown.wait_element_without_error().is_displayed()
    assert all((initial_not_displayed, after_hover_displayed))


def test_screenshot(base_playground_page, driver_engine, driver_name, platform, request):
    node_name = request.node.name.replace('_', '-')
    filename = f'{node_name}-{driver_engine}-{driver_name}-{platform}-kube'
    base_playground_page.kube.scroll_into_view(sleep=0.5).assert_screenshot(filename, threshold=6)


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

    all_cards[2].button.click()
    assert MouseEventPage().wait_page_loaded().is_page_opened()
