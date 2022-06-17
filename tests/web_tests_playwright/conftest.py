import pytest
from playwright.sync_api import sync_playwright
from dyatel.dyatel_play.web_driver import WebDriver

from dyatel.utils import set_logging_settings


set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')


@pytest.fixture
def playwright_driver(request):
    with sync_playwright() as connect:
        is_headless = request.config.getoption('headless')
        playwright_driver = connect.chromium.launch(headless=is_headless)
        driver = WebDriver(driver=playwright_driver)
        yield driver
        driver.driver.close()
