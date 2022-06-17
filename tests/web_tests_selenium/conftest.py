import os

import pytest
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as GeckoWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from data_for_testing.settings import android_desired_caps
from data_for_testing.utils import set_logging_settings
from selenium_master.driver.mobile_driver import MobileDriver
from selenium_master.driver.web_driver import WebDriver
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage

set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Run in headless mode')
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


@pytest.fixture
def driver_wrapper(driver, driver_name, markers, request):
    xfail_marks_iterator = tuple(request.node.iter_markers(name='xfail_platform'))
    xfail_platform = list(name for marker in xfail_marks_iterator for name in marker.args)

    if driver_name in xfail_platform:
        xfail_reason = list(name for marker in xfail_marks_iterator for name in marker.kwargs.values())
        pytest.xfail(f"Expected failed for {driver_name}. Reason={xfail_reason}")

    if driver_name in ('android', 'ios'):
        driver_wrapper = MobileDriver(driver=driver)
    else:
        driver_wrapper = WebDriver(driver=driver)

    yield driver_wrapper
    driver_wrapper.driver.get('data:,')


@pytest.fixture
def markers(request):
    return request.node.own_markers


@pytest.fixture(scope='session')
def driver(chrome_options, firefox_options, driver_name, request):
    driver = None
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    is_mobile = driver_name in ('android', 'ios')

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


@pytest.fixture
def base_playground_page(driver_wrapper):
    return PlaygroundMainPage().open_page()


@pytest.fixture
def pizza_order_page(driver_wrapper):
    return PizzaOrderPage().open_page()
