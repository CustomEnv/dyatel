import random

import pytest

from dyatel.exceptions import NoSuchElementException
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
    """ all_elements when parent of Element is other element """
    all_elements = base_playground_page.any_div_with_parent.all_elements
    assert all_elements, 'did not find elements on page'

    for element in all_elements:
        assert element.parent == base_playground_page.any_section


def test_element_group_all_elements_child(second_playground_page):
    """ all_elements when parent of Element is Group """
    all_cards = second_playground_page.get_all_cards()

    for index, element_object in enumerate(all_cards):
        if 0 < index < len(all_cards) - 1:
            assert element_object.button.element != all_cards[index - 1].button.element
            assert element_object.button.element != all_cards[index + 1].button.element

    all_cards[1].button.click()
    assert KeyboardPage().wait_page_loaded().is_page_opened()
