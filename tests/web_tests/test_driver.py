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

