import pytest
from playwright.sync_api import sync_playwright
from playwright_master.web_driver import WebDriver

from data_for_testing.utils import set_logging_settings, sidebar_page_path, tabs_page_path
from data_for_testing.web.playwright.pages.sidebar_page import SidebarPagePlaywright
from data_for_testing.web.playwright.pages.tabs_page import TabsPagePlaywright


set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')


@pytest.fixture
def playwright_driver(request):
    with sync_playwright() as connect:
        is_headless = request.config.getoption('headless')
        playwright_driver = connect.chromium.launch(headless=is_headless)
        driver = WebDriver(driver=playwright_driver)
        all_pytest_markers = [marker.name for marker in request.node.own_markers]
        yield driver
        if 'no_teardown' not in all_pytest_markers:
            driver.driver.close()


@pytest.fixture
def sidebar_page(playwright_driver):
    page = SidebarPagePlaywright().get(url=sidebar_page_path)
    return page


@pytest.fixture
def tabs_page(playwright_driver):
    page = TabsPagePlaywright().get(url=tabs_page_path)
    return page
