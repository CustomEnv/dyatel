import os

import pytest
from playwright.sync_api import sync_playwright
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as GeckoWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from dyatel.base.driver import Driver
from tests.settings import android_desired_caps, ios_desired_caps
from dyatel.utils import set_logging_settings
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage


set_logging_settings()


# FIXME: other Group or Page as class variable of Group or Page -> mb will be skipped


def pytest_addoption(parser):
    parser.addoption('--engine', default='selenium', help='Specify driver engine')
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Browser name')
    parser.addoption('--platform', default='desktop', help='Platform name')
    parser.addoption('--appium-port', default='1000')
    parser.addoption('--appium-ip', default='0.0.0.0')


@pytest.fixture(scope='session')
def driver_name(request):
    return request.config.getoption('driver').lower()


@pytest.fixture(scope='session')
def driver_engine(request):
    return request.config.getoption('engine').lower()


@pytest.fixture(scope='session')
def platform(request):
    return request.config.getoption('platform').lower()


@pytest.fixture(scope='session')
def chrome_options(request):
    options = ChromeOptions()
    if request.config.getoption('headless'):
        options.headless = True
    return options


@pytest.fixture(scope='session')
def firefox_options(request):
    options = FirefoxOptions()
    if request.config.getoption('headless'):
        options.headless = True
    return options


@pytest.fixture
def driver_wrapper(platform, driver_name, driver_engine, request, driver):
    xfail_marks_iterator = tuple(request.node.iter_markers(name='xfail_platform'))
    xfail_platform = list(name for marker in xfail_marks_iterator for name in marker.args)

    if platform in xfail_platform or driver_engine in xfail_platform:
        xfail_reason = list(name for marker in xfail_marks_iterator for name in marker.kwargs.values())
        pytest.xfail(f"Expected failed for {platform} with {driver_name}. Reason={xfail_reason}")

    driver_wrapper = Driver(driver)

    yield driver_wrapper
    driver_wrapper.get('data:,')


@pytest.fixture
def markers(request):
    return request.node.own_markers


@pytest.fixture(scope='session')
def driver(request, driver_name, driver_engine, chrome_options, firefox_options, platform):
    driver = None
    is_headless = request.config.getoption('headless')

    if 'appium' in driver_engine:
        appium_ip = request.config.getoption('--appium-ip')
        appium_port = request.config.getoption('--appium-port')
        command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'

        caps = android_desired_caps if platform == 'android' else ios_desired_caps
        caps.update({'browserName': driver_name.title()})
        driver = AppiumDriver(command_executor=command_exc, desired_capabilities=caps)

        yield driver
        driver.quit()  # FIXME

    elif 'selenium' in driver_engine:
        if driver_name == 'chrome':
            driver = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=chrome_options)
        elif driver_name == 'firefox':
            driver = GeckoWebDriver(executable_path=GeckoDriverManager().install(), options=firefox_options)
        elif driver_name == 'safari':
            driver = SafariWebDriver()

        driver.implicitly_wait(0.01)  # FIXME
        driver.set_window_size(1024, 900)  # FIXME
        driver.set_window_position(0, 0)  # FIXME

        yield driver
        driver.quit()  # FIXME

    elif 'play' in driver_engine:
        with sync_playwright() as playwright:
            if driver_name == 'chrome':
                browser = playwright.chromium
            elif driver_name == 'firefox':
                browser = playwright.firefox
            elif driver_name == 'safari':
                browser = playwright.webkit

            driver = browser.launch(headless=is_headless)
            yield driver
            driver.close()  # FIXME

    assert driver, 'Driver isn\'t selected. Check your settings'


@pytest.fixture
def base_playground_page(driver_wrapper):
    return PlaygroundMainPage().open_page()


@pytest.fixture
def pizza_order_page(driver_wrapper):
    return PizzaOrderPage().open_page()


@pytest.fixture
def mouse_event_page(driver_wrapper):
    return MouseEventPage().open_page()
