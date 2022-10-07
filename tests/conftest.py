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

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.shared_utils import set_logging_settings
from dyatel.visual_comparison import VisualComparison
from tests.adata.pages.expected_condition_page import ExpectedConditionPage
from tests.adata.pages.forms_page import FormsPage
from tests.adata.pages.keyboard_page import KeyboardPage
from tests.adata.pages.progress_bar_page import ProgressBarPage
from tests.settings import android_desired_caps, ios_desired_caps
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage, SecondPlaygroundMainPage


set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--engine', default='selenium', help='Specify driver engine')
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Browser name')
    parser.addoption('--platform', default='desktop', help='Platform name')
    parser.addoption('--generate-reference', action='store_true', help='Generate reference images in visual tests')
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


@pytest.fixture
def markers(request):
    return request.node.own_markers


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
def driver_wrapper(platform, driver_name, driver_engine, request, driver_init):
    skip_marks_iterator = tuple(request.node.iter_markers(name='skip_platform'))
    skip_platform = list(name for marker in skip_marks_iterator for name in marker.args)
    xfail_marks_iterator = tuple(request.node.iter_markers(name='xfail_platform'))
    xfail_platform = list(name for marker in xfail_marks_iterator for name in marker.args)

    if platform in str(xfail_platform) or driver_engine in str(xfail_platform) or driver_name in str(xfail_platform):
        xfail_reason = list(name for marker in xfail_marks_iterator for name in marker.kwargs.values())
        pytest.xfail(f"Expected failed for {platform} with {driver_name}. Reason={xfail_reason}")

    if platform in str(skip_platform) or driver_engine in str(skip_platform) or driver_name in str(skip_platform):
        skip_reason = list(name for marker in skip_marks_iterator for name in marker.kwargs.values())
        pytest.skip(f"Skip test {platform} with {driver_name}. Reason={skip_reason}")

    yield driver_init
    driver_init.get('data:,')


@pytest.fixture
def second_driver_wrapper(request, driver_name, driver_engine, chrome_options, firefox_options, platform):
    driver = driver_func(request, driver_name, driver_engine, chrome_options, firefox_options, platform)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def driver_init(request, driver_name, driver_engine, chrome_options, firefox_options, platform):
    driver = driver_func(request, driver_name, driver_engine, chrome_options, firefox_options, platform)
    yield driver
    driver.quit()


def driver_func(request, driver_name, driver_engine, chrome_options, firefox_options, platform):
    driver, browser = None, None
    is_headless = request.config.getoption('headless')

    if 'appium' in driver_engine:
        if not DriverWrapper.driver:
            appium_ip = request.config.getoption('--appium-ip')
            appium_port = request.config.getoption('--appium-port')
            command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
            is_android = platform == 'android'
            caps = android_desired_caps if is_android else ios_desired_caps

            caps.update({'browserName': driver_name.title()})

            if is_android:
                caps.update({'chromedriverArgs': ['--hide-scrollbars']})

            driver = AppiumDriver(command_executor=command_exc, desired_capabilities=caps)
        else:
            driver = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=chrome_options)

    elif 'selenium' in driver_engine:
        if driver_name == 'chrome':
            driver = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=chrome_options)
        elif driver_name == 'firefox':
            driver = GeckoWebDriver(executable_path=GeckoDriverManager().install(), options=firefox_options)
        elif driver_name == 'safari':
            if not DriverWrapper.driver:
                driver = SafariWebDriver()
            else:
                driver = ChromeWebDriver(executable_path=ChromeDriverManager().install(), options=chrome_options)

        driver.set_window_position(0, 0)  # FIXME

    elif 'play' in driver_engine:
        driver = PlayDriver.instance

        if not driver:
            playwright = sync_playwright().start()

            if driver_name == 'chrome':
                browser = playwright.chromium
            elif driver_name == 'firefox':
                browser = playwright.firefox
            elif driver_name == 'safari':
                browser = playwright.webkit

            driver = browser.launch(headless=is_headless)

    driver_wrapper = DriverWrapper(driver)

    VisualComparison.visual_regression_path = os.path.dirname(os.path.abspath(__file__)) + '/adata/visual'
    VisualComparison.visual_reference_generation = request.config.getoption('--generate-reference')

    if 'appium' not in driver_engine:
        driver_wrapper.set_window_size(1024, 900)

    return driver_wrapper


@pytest.fixture
def base_playground_page(driver_wrapper):
    return PlaygroundMainPage().open_page()


@pytest.fixture
def second_playground_page(driver_wrapper):
    return SecondPlaygroundMainPage().open_page()


@pytest.fixture
def pizza_order_page(driver_wrapper):
    return PizzaOrderPage().open_page()


@pytest.fixture
def mouse_event_page(driver_wrapper):
    return MouseEventPage().open_page()


@pytest.fixture
def forms_page(driver_wrapper):
    return FormsPage().open_page()


@pytest.fixture
def expected_condition_page(driver_wrapper):
    return ExpectedConditionPage().open_page().set_min_and_max_wait()


@pytest.fixture
def progressbar_page(driver_wrapper):
    return ProgressBarPage().open_page()


@pytest.fixture
def keyboard_page(driver_wrapper):
    return KeyboardPage().open_page()
