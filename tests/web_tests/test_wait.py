import pytest

from dyatel.exceptions import UnexpectedElementsCountException


# TODO: rework needed
def test_wait_element(pizza_order_page):
    pizza_order_page.submit_button.wait_element()
    assert pizza_order_page.submit_button.is_displayed()


# TODO: rework needed
def test_wait_without_error(pizza_order_page):
    pizza_order_page.error_modal.wait_element_without_error(timeout=0.5)
    assert not pizza_order_page.error_modal.is_displayed()


# TODO: rework needed
def test_wait_hidden(pizza_order_page):
    pizza_order_page.error_modal.wait_element_without_error(timeout=1)
    assert not pizza_order_page.error_modal.is_displayed()


# TODO: rework needed
def test_wait_hidden_without_error(pizza_order_page):
    pizza_order_page.submit_button.wait_element_without_error(timeout=0.5)
    assert pizza_order_page.submit_button.is_displayed()


@pytest.mark.xfail_platform('android', 'ios', reason='Can not get value from that element. TODO: Rework test')
def test_wait_element_value(expected_condition_page):
    expected_condition_page.value_card.trigger_button.click()
    value_without_wait = expected_condition_page.value_card.wait_for_value_input.value
    expected_condition_page.value_card.wait_for_value_input.wait_element_value()
    value_with_wait = expected_condition_page.value_card.wait_for_value_input.value == 'Dennis Ritchie'
    assert all((not value_without_wait, value_with_wait))


@pytest.mark.xfail_platform('playwright', 'safari', reason='Unexpected text')
def test_wait_element_text(expected_condition_page):
    btn = expected_condition_page.value_card.wait_for_text_button

    expected_condition_page.value_card.trigger_button.click()
    value_without_wait = btn.text
    value_with_wait = btn.wait_element_text().text == 'Submit'
    assert all((not value_without_wait, value_with_wait))


def test_wait_elements_count_v1(forms_page):
    forms_page.validation_form.form_mixin.input.type_text('sample')
    forms_page.validation_form.submit_form_button.click()
    forms_page.validation_form.any_error.wait_elements_count(4)
    assert forms_page.validation_form.any_error.get_elements_count() == 4


def test_wait_elements_count_v2(expected_condition_page):
    initial_count = expected_condition_page.frame_card.frame.get_elements_count()
    expected_condition_page.frame_card.trigger_button.click()
    target_count = expected_condition_page.frame_card.frame.wait_elements_count(1).get_elements_count()
    assert all((initial_count == 0, target_count == 1))


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
