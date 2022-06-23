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

from tests.settings import android_desired_caps
from dyatel.utils import set_logging_settings
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.dyatel_play.play_driver import PlayDriver
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage


set_logging_settings()


# FIXME: other Group or Page as class variable of Group or Page -> mb will be skipped
# FIXME: make "silent" argument latest
# FIXME: group with parent group (with element in init) seems doesn't set "parent" for element


def pytest_addoption(parser):
    parser.addoption('--engine', default='selenium', help='Specify driver engine')
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Driver selecting')
    parser.addoption('--appium-port', default='1000')
    parser.addoption('--appium-ip', default='0.0.0.0')


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


@pytest.fixture(scope='session')
def driver_name(request):
    return request.config.getoption('driver').lower()


@pytest.fixture(scope='session')
def driver_engine(request):
    return request.config.getoption('engine').lower()


@pytest.fixture
def driver_wrapper(driver, driver_name, markers, driver_engine, request):
    xfail_marks_iterator = tuple(request.node.iter_markers(name='xfail_platform'))
    xfail_platform = list(name for marker in xfail_marks_iterator for name in marker.args)

    if driver_name in xfail_platform or driver_engine in xfail_platform:
        xfail_reason = list(name for marker in xfail_marks_iterator for name in marker.kwargs.values())
        pytest.xfail(f"Expected failed for {driver_name}. Reason={xfail_reason}")

    if driver_name in ('android', 'ios'):
        driver_wrapper = MobileDriver(driver=driver)
    elif 'selenium' in driver_engine:
        driver_wrapper = WebDriver(driver=driver)
    elif 'play' in driver_engine:
        driver_wrapper = PlayDriver(driver=driver)
    else:
        raise Exception('Cant specify driver wrapper with given settings')

    yield driver_wrapper
    driver_wrapper.get('data:,')


@pytest.fixture
def markers(request):
    return request.node.own_markers


@pytest.fixture(scope='session')
def driver(chrome_options, firefox_options, driver_name, driver_engine, request):
    driver = None
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    is_mobile = driver_name in ('android', 'ios')
    is_headless = request.config.getoption('headless')

    if 'selenium' in driver_engine:
        if driver_name == 'chrome':
            driver = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=chrome_options)
        elif driver_name == 'firefox':
            driver = GeckoWebDriver(executable_path=GeckoDriverManager().install(), options=firefox_options)
        elif driver_name == 'safari':
            driver = SafariWebDriver()
        elif driver_name == 'android':
            os.environ['mobile'] = 'True'
            android_desired_caps.update({'browserName': 'Chrome'})
            driver = AppiumDriver(command_executor=command_exc, desired_capabilities=android_desired_caps)
            driver.use_selenium_search = True

        if not is_mobile:
            driver.implicitly_wait(0.01)
            driver.set_window_size(1024, 900)
            driver.set_window_position(0, 0)

        yield driver
        driver.quit()

    elif 'play' in driver_engine:
        with sync_playwright() as connect:
            driver = connect.chromium.launch(headless=is_headless)
            yield driver
            driver.close()

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
