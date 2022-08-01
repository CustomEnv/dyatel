import pytest

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
    assert driver_wrapper.execute_script('return document.title;') == 'Mouse Actions'


def test_driver_execute_script_with_args(driver_wrapper, mouse_event_page):
    driver_wrapper.execute_script('arguments[0].click();', mouse_event_page.header_logo.element)
    assert SecondPlaygroundMainPage().wait_page_loaded().is_page_opened()


@pytest.mark.skip_platform(
    'appium', 'safari',  # FIXME: Unskip for playwright safari
    reason='Safari browser/Mobile platforms doesnt support multiple drivers'
)
def test_second_driver_different_page(driver_wrapper, second_driver_wrapper):
    mouse_page = MouseEventPage().set_driver(second_driver_wrapper)
    pizza_page = PizzaOrderPage().set_driver(driver_wrapper)

    assert pizza_page.driver != mouse_page.driver
    assert pizza_page.driver_wrapper != mouse_page.driver_wrapper
    assert mouse_page.header_logo.driver != pizza_page.quantity_input.driver
    assert mouse_page.header_logo.driver_wrapper != pizza_page.quantity_input.driver_wrapper

    mouse_page.open_page()
    pizza_page.open_page()

    assert mouse_page.is_page_opened()
    assert mouse_page.header_logo.is_displayed()

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()


@pytest.mark.skip_platform(
    'appium', 'safari',  # FIXME: Unskip for playwright safari
    reason='Safari browser/Mobile platforms doesnt support multiple drivers'
)
def test_second_driver_same_page(driver_wrapper, second_driver_wrapper):
    mouse_page1 = MouseEventPage().set_driver(second_driver_wrapper)
    mouse_page2 = MouseEventPage().set_driver(driver_wrapper)

    assert mouse_page1.driver != mouse_page2.driver
    assert mouse_page1.driver_wrapper != mouse_page2.driver_wrapper
    assert mouse_page1.header_logo.driver != mouse_page2.header_logo.driver
    assert mouse_page1.header_logo.driver_wrapper != mouse_page2.header_logo.driver_wrapper

    mouse_page1.open_page()
    mouse_page2.open_page()

    assert mouse_page1.is_page_opened()
    assert mouse_page2.is_page_opened()


@pytest.mark.skip_platform(
    'appium', 'safari',  # FIXME: Unskip for playwright safari
    reason='Safari browser/Mobile platforms doesnt support multiple drivers'
)
def test_second_driver_by_arg(driver_wrapper, second_driver_wrapper):
    mouse_page = MouseEventPage(second_driver_wrapper)
    pizza_page = PizzaOrderPage(driver_wrapper)

    assert pizza_page.driver != mouse_page.driver
    assert pizza_page.driver_wrapper != mouse_page.driver_wrapper
    assert mouse_page.header_logo.driver != pizza_page.quantity_input.driver
    assert mouse_page.header_logo.driver_wrapper != pizza_page.quantity_input.driver_wrapper

    mouse_page.open_page()
    pizza_page.open_page()

    assert mouse_page.is_page_opened()
    assert mouse_page.header_logo.is_displayed()

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()


@pytest.mark.skip_platform(
    'appium',
    reason='Appium doesnt support tabs creating'
)
def test_driver_tabs(driver_wrapper, second_playground_page):
    driver_wrapper.create_new_tab()
    driver_wrapper.switch_to_original_tab()
    driver_wrapper.switch_to_tab(2)
    driver_wrapper.create_new_tab()
    driver_wrapper.close_unused_tabs()
