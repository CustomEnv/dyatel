import pytest
from mock.mock import MagicMock

from playwright.sync_api import Browser, Page as PlaywrightSourcePage
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper, DriverWrapperSessions
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_driver import CoreDriver


@pytest.fixture
def mocked_shared_mobile_driver():
    appium_driver = AppiumDriver
    appium_driver.__init__ = lambda *args, **kwargs: None
    appium_driver.session_id = None
    appium_driver.command_executor = MagicMock()
    appium_driver.error_handler = MagicMock()
    return appium_driver


@pytest.fixture
def mocked_ios_driver(mocked_shared_mobile_driver):
    mocked_shared_mobile_driver.capabilities = MagicMock(
        return_value={
            'platformName': 'ios',
            'browserName': 'safari',
            'automationName': 'safari'
        }
    )()
    driver_wrapper = DriverWrapper(mocked_shared_mobile_driver())
    return driver_wrapper


@pytest.fixture
def mocked_android_driver(mocked_shared_mobile_driver):
    mocked_shared_mobile_driver.capabilities = MagicMock(
        return_value={
            'platformName': 'Android',
            'browserName': 'chrome',
            'automationName': 'UiAutomator2'
        }
    )()
    driver_wrapper = DriverWrapper(mocked_shared_mobile_driver())
    return driver_wrapper


@pytest.fixture
def mocked_selenium_driver():
    selenium_driver = SeleniumDriver
    selenium_driver.__init__ = lambda *args, **kwargs: None
    selenium_driver.session_id = None
    selenium_driver.command_executor = MagicMock()
    selenium_driver.error_handler = MagicMock()

    driver_wrapper = DriverWrapper(selenium_driver())
    return driver_wrapper


@pytest.fixture
def mocked_play_driver():
    driver_wrapper = DriverWrapper(Browser(MagicMock()))
    driver_wrapper.driver = PlaywrightSourcePage(MagicMock())
    return driver_wrapper


@pytest.fixture(autouse=True)
def base_teardown():
    yield
    DriverWrapper.is_multiplatform = False
    DriverWrapper.is_mobile = False
    DriverWrapper.is_desktop = False
    DriverWrapper.is_ios = False
    DriverWrapper.is_android = False
    DriverWrapper.is_selenium = False
    DriverWrapper.is_playwright = False
    PlayDriver.driver = None
    CoreDriver.driver = None
    DriverWrapperSessions.all_sessions = []


mobile_drivers = [mocked_ios_driver.__name__, mocked_android_driver.__name__]
mobile_ids = ['appium ios', 'appium android']


desktop_drivers = [mocked_selenium_driver.__name__, mocked_play_driver.__name__]
desktop_ids = ['selenium', 'playwright']


all_drivers = mobile_drivers + desktop_drivers
all_ids = mobile_ids + desktop_ids


selenium_drivers = [mocked_selenium_driver.__name__] + mobile_drivers
selenium_ids = ['selenium'] + mobile_ids
