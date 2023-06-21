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
from dyatel.shared_utils import disable_logging
from dyatel.utils.logs import dyatel_logs_settings
from dyatel.visual_comparison import VisualComparison
from tests.adata.pages.expected_condition_page import ExpectedConditionPage
from tests.adata.pages.forms_page import FormsPage
from tests.adata.pages.frames_page import FramesPage
from tests.adata.pages.keyboard_page import KeyboardPage
from tests.adata.pages.progress_bar_page import ProgressBarPage
from tests.settings import android_desired_caps, ios_desired_caps
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage, SecondPlaygroundMainPage


dyatel_logs_settings()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Browser name')
    parser.addoption('--platform', default='selenium', help='Platform name')
    parser.addoption('--gr', action='store_true', help='Generate reference images in visual tests')
    parser.addoption('--sv', action='store_true', help='Generate reference images in visual tests')
    parser.addoption('--hgr', action='store_true', help='Hard generate reference images in visual tests')
    parser.addoption('--appium-port', default='1000')
    parser.addoption('--appium-ip', default='0.0.0.0')


@pytest.fixture(scope='session')
def driver_name(request):
    return request.config.getoption('driver').lower()


@pytest.fixture(scope='session')
def platform(request):
    return request.config.getoption('platform').lower()


@pytest.fixture(scope='session')
def chrome_options(request):
    options = ChromeOptions()
    if request.config.getoption('headless'):
        options.headless = True
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    return options


@pytest.fixture(scope='session')
def firefox_options(request):
    options = FirefoxOptions()
    if request.config.getoption('headless'):
        options.headless = True
    return options


@pytest.fixture
def driver_wrapper(platform, driver_name, driver_init):
    # Prints are required for better readability: https://github.com/pytest-dev/pytest/issues/8574
    print()
    yield driver_init
    print()
    driver_init.get('data:,', silent=True)


@pytest.fixture
def second_driver_wrapper(request, driver_name, platform, chrome_options, firefox_options):
    driver = driver_func(request, driver_name, platform, chrome_options, firefox_options)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def driver_init(request, driver_name, platform, chrome_options, firefox_options):
    driver = driver_func(request, driver_name, platform, chrome_options, firefox_options)
    yield driver
    driver.quit(silent=True)


def driver_func(request, driver_name, platform, chrome_options, firefox_options):
    driver, browser = None, None
    is_mobile = platform in ('ios', 'android')

    if is_mobile:
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

    elif 'selenium' in platform:
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

    elif 'playwright' in platform:
        driver = PlayDriver.instance

        if not driver:
            playwright = sync_playwright().start()

            if driver_name == 'chrome':
                browser = playwright.chromium
            elif driver_name == 'firefox':
                browser = playwright.firefox
            elif driver_name == 'safari':
                browser = playwright.webkit

            driver = browser.launch(headless=request.config.getoption('headless'))

    driver_wrapper = DriverWrapper(driver)

    VisualComparison.visual_regression_path = os.path.dirname(os.path.abspath(__file__)) + '/adata/visual'
    VisualComparison.visual_reference_generation = request.config.getoption('--gr')
    VisualComparison.hard_visual_reference_generation = request.config.getoption('--hgr')
    VisualComparison.skip_screenshot_comparison = request.config.getoption('--sv')
    VisualComparison.default_threshold = 0.1

    if not is_mobile:
        driver_wrapper.set_window_size(1024, 900)

    return driver_wrapper


def skip_platform(item: pytest.Item, platform: str):
    """
    Skip test on given platform in args

    Example::
      @pytest.mark.skip_platform('ios', reason='Fix needed')
      @pytest.mark.skip_platform(platform='desktop', reason='Fix needed')

    :param item: test function object ~ <function test_non_adult_sign_up_dialogue_and_links at 0x10ad658b0>
    :param platform: current platform name ~ selenium, playwright, appium
    :return: None
    """
    skip_platform_marker = item.get_closest_marker('skip_platform')
    skip_platform_kwargs = getattr(skip_platform_marker, 'kwargs', {})

    if platform in str(getattr(skip_platform_marker, 'args', [])):
        skip_message = f"Skip platform {platform}. Reason={skip_platform_kwargs.get('reason')}"
        item.add_marker(pytest.mark.skip(skip_message))


def pytest_collection_modifyitems(items):
    for item in items:
        skip_platform(item=item, platform=item.session.config.getoption("--platform"))


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


@pytest.fixture
def frames_page(driver_wrapper):
    return FramesPage().open_page()