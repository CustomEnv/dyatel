import time

import pytest


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
