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
def test_second_driver(driver_wrapper, second_driver_wrapper):
    second_driver_wrapper.get(MouseEventPage().url)
    driver_wrapper.get(PizzaOrderPage().url)

    assert MouseEventPage().set_driver(second_driver_wrapper).is_page_opened()
    assert MouseEventPage().header_logo.is_displayed()

    assert PizzaOrderPage().set_driver(driver_wrapper).is_page_opened()
    assert PizzaOrderPage().quantity_input.is_displayed()
