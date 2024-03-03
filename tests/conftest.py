import os

import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.utils.logs import dyatel_logs_settings
from dyatel.visual_comparison import VisualComparison
from tests.adata.drivers.driver_entities import DriverEntities
from tests.adata.drivers.driver_factory import DriverFactory
from tests.adata.pages.expected_condition_page import ExpectedConditionPage
from tests.adata.pages.forms_page import FormsPage
from tests.adata.pages.frames_page import FramesPage
from tests.adata.pages.keyboard_page import KeyboardPage
from tests.adata.pages.progress_bar_page import ProgressBarPage
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage
from tests.adata.pages.playground_main_page import PlaygroundMainPage, SecondPlaygroundMainPage
from tests.adata.pytest_utils import skip_platform


dyatel_logs_settings()


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run in headless mode')
    parser.addoption('--driver', default='chrome', help='Browser name')
    parser.addoption('--platform', default='selenium', help='Platform name')
    parser.addoption('--gr', action='store_true', help='Generate reference images in visual tests')
    parser.addoption('--sv', action='store_true', help='Generate reference images in visual tests')
    parser.addoption('--hgr', action='store_true', help='Hard generate reference images in visual tests')
    parser.addoption('--sgr', action='store_true', help='Soft generate reference images in visual tests')
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


@pytest.fixture(autouse=True)
def redirect(request):
    # Prints are required for better readability: https://github.com/pytest-dev/pytest/issues/8574
    print()
    yield
    print()
    if DriverWrapper.session.sessions_count() > 0:
        driver_wrapper = request.getfixturevalue('driver_wrapper')
        driver_wrapper.get('data:,', silent=True)


@pytest.fixture
def second_driver_wrapper(request, driver_name, platform, chrome_options, firefox_options):
    driver = driver_func(**locals())
    yield driver
    driver.quit(silent=True)


@pytest.fixture(scope='session')
def driver_wrapper(request, driver_name, platform, chrome_options, firefox_options):
    driver = driver_func(**locals())
    yield driver
    driver.quit(silent=True)


def driver_func(request, driver_name, platform, chrome_options, firefox_options):
    entities = DriverEntities(request, driver_name, platform, chrome_options, firefox_options)
    driver = DriverFactory.create_driver(entities)

    driver_wrapper = DriverWrapper(driver)

    if driver_wrapper.is_desktop:
        driver_wrapper.set_window_size(1024, 900)

    return driver_wrapper


@pytest.fixture(autouse=True)
def visual_comparisons_settings(request):
    VisualComparison.visual_regression_path = os.path.dirname(os.path.abspath(__file__)) + '/adata/visual'
    VisualComparison.visual_reference_generation = request.config.getoption('--gr')
    VisualComparison.hard_visual_reference_generation = request.config.getoption('--hgr')
    VisualComparison.soft_visual_reference_generation = request.config.getoption('--sgr')
    VisualComparison.skip_screenshot_comparison = request.config.getoption('--sv')
    VisualComparison.default_threshold = 0.1
    VisualComparison.test_item = request.node


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
