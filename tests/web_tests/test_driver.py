import pytest

from dyatel.base.driver_wrapper import DriverWrapper
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import SecondPlaygroundMainPage


def test_driver_cookies(driver_wrapper, mouse_event_page):
    driver_wrapper.set_cookie([{'name': 'sample_cookie', 'value': '123', 'path': '/', 'domain': 'http://example'}])

    actual_cookies_after_set = driver_wrapper.get_cookies()
    driver_wrapper.clear_cookies()
    actual_cookies_after_clear = driver_wrapper.get_cookies()

    assert all((actual_cookies_after_set, not actual_cookies_after_clear))


def test_driver_execute_script_set_and_get(driver_wrapper, mouse_event_page):
    driver_wrapper.execute_script('sessionStorage.setItem("foo", "bar")')
    assert driver_wrapper.execute_script('return sessionStorage.getItem("foo")') == 'bar'


def test_driver_execute_script_return_value(driver_wrapper, mouse_event_page):
    assert driver_wrapper.execute_script('return document.title;') == 'Mouse Actions v2'


def test_driver_execute_script_with_args(driver_wrapper, mouse_event_page):
    driver_wrapper.execute_script('arguments[0].click();', mouse_event_page.header_logo.element)
    assert SecondPlaygroundMainPage().wait_page_loaded().is_page_opened()


def test_second_driver_different_page(driver_wrapper, second_driver_wrapper):
    mouse_page = MouseEventPage(second_driver_wrapper)
    pizza_page = PizzaOrderPage(driver_wrapper)
    assert len(DriverWrapper.session.all_sessions) == 2

    mouse_page.open_page()
    pizza_page.open_page()

    assert pizza_page.driver is not mouse_page.driver
    assert pizza_page.driver_wrapper is not mouse_page.driver_wrapper
    assert mouse_page.header_logo.driver is not pizza_page.quantity_input.driver
    assert mouse_page.header_logo.driver_wrapper is not pizza_page.quantity_input.driver_wrapper

    assert mouse_page.is_page_opened()
    assert mouse_page.header_logo.is_displayed()

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()


def test_second_driver_same_page(driver_wrapper, second_driver_wrapper):
    mouse_page1 = MouseEventPage(driver_wrapper)
    mouse_page2 = MouseEventPage(second_driver_wrapper)
    assert len(DriverWrapper.session.all_sessions) == 2

    mouse_page1.open_page()
    mouse_page2.open_page()

    assert mouse_page2.driver is not mouse_page1.driver
    assert mouse_page2.driver_wrapper is not mouse_page1.driver_wrapper
    assert mouse_page2.header_logo.driver is not mouse_page1.header_logo.driver
    assert mouse_page2.header_logo.driver_wrapper is not mouse_page1.header_logo.driver_wrapper

    assert mouse_page2.is_page_opened()
    assert mouse_page1.is_page_opened()


def test_second_driver_by_arg(driver_wrapper, second_driver_wrapper):
    pizza_page = PizzaOrderPage(driver_wrapper)
    mouse_page = MouseEventPage(second_driver_wrapper)
    assert len(DriverWrapper.session.all_sessions) == 2

    mouse_page.open_page()
    pizza_page.open_page()

    assert pizza_page.driver_wrapper is not mouse_page.driver_wrapper
    assert pizza_page.driver is not mouse_page.driver
    assert mouse_page.header_logo.driver is not pizza_page.quantity_input.driver
    assert mouse_page.header_logo.driver_wrapper is not pizza_page.quantity_input.driver_wrapper

    assert mouse_page.is_page_opened()
    assert mouse_page.header_logo.is_displayed()

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()


def test_second_driver_compatibility(driver_wrapper, second_driver_wrapper):
    assert driver_wrapper.get_inner_window_size()
    assert second_driver_wrapper.get_inner_window_size()


@pytest.mark.skip_platform('android', 'ios', reason='Appium doesnt support tabs creating')
def test_driver_tabs(driver_wrapper, second_playground_page):
    driver_wrapper.create_new_tab()
    driver_wrapper.switch_to_original_tab()
    driver_wrapper.switch_to_tab()
    driver_wrapper.switch_to_tab(1)
    driver_wrapper.create_new_tab()
    driver_wrapper.close_unused_tabs()


def test_parent_in_hidden_element(driver_wrapper, second_driver_wrapper):
    pizza_page = PizzaOrderPage(driver_wrapper)
    mouse_page = MouseEventPage(second_driver_wrapper)

    card = mouse_page.mouse_click_card()

    mouse_page.open_page()
    pizza_page.open_page()

    assert DriverWrapper.driver

    assert mouse_page.is_page_opened()
    assert mouse_page.button_with_text('Drop me').wait_element(2).is_displayed()  # button without specified driver

    assert card.any_button.parent == card
    assert card.any_button_without_parent.parent is False
    assert card.any_button_with_custom_parent.parent == card.y_result

    assert pizza_page.is_page_opened()
    assert pizza_page.input_with_value('SMALL').wait_element(2).is_displayed()  # button without specified driver


def test_driver_in_hidden_group(driver_wrapper, second_driver_wrapper):
    pizza_page = PizzaOrderPage(driver_wrapper)
    mouse_page = MouseEventPage(second_driver_wrapper)

    mouse_page.open_page()
    pizza_page.open_page()

    assert mouse_page.is_page_opened()
    assert mouse_page.mouse_click_card().is_displayed()  # mouse_click_card without specified driver
    assert mouse_page.mouse_click_card().click_area.parent.is_displayed()
    assert mouse_page.mouse_click_card().click_area.element  # can fail on unexpected __call__ to object
    assert mouse_page.mouse_click_card().click_area.is_displayed()  # can fail on unexpected __call__ to parent

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()


def test_driver_in_hidden_page(driver_wrapper, second_driver_wrapper):
    base_page1 = SecondPlaygroundMainPage(driver_wrapper).open_page()
    base_page2 = SecondPlaygroundMainPage(second_driver_wrapper).open_page()

    exp_cond_page = base_page1.navigate_to_expected_condition_page()  # page class without specified driver
    keyboard_page = base_page2.navigate_to_keyboard_page()  # page class without specified driver

    assert exp_cond_page.max_wait_input.wait_element(2).is_displayed()
    assert keyboard_page.input_area.wait_element(2).is_displayed()


def test_second_driver_in_parent_element(driver_wrapper, second_driver_wrapper):
    mouse_page2 = MouseEventPage(second_driver_wrapper)
    mouse_page2.open_page()
    card = mouse_page2.drag_n_drop()

    assert card.drag_target.parent._initialized
    assert card.card_body._initialized

    assert card.card_body.parent == card
    assert card.drag_target.parent.parent == card
    assert card.drag_target.parent.locator == card.card_body.locator

    assert mouse_page2.is_page_opened()
    assert card.drag_target.is_displayed()

    assert card.drag_target.parent.driver_wrapper == second_driver_wrapper
    assert card.card_body.driver_wrapper == second_driver_wrapper
