import pytest
from mock.mock import MagicMock

from playwright.sync_api import Page as PlaywrightDriver, Browser
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver


@pytest.fixture
def mocked_mobile_driver():
    appium_driver = AppiumDriver
    appium_driver.__init__ = lambda *args, **kwargs: None
    appium_driver.session_id = None
    appium_driver.command_executor = MagicMock()
    appium_driver.error_handler = MagicMock()

    appium_driver.capabilities = MagicMock(return_value={
        'platformName': 'ios', 'browserName': 'safari', 'automationName': 'safari'
    })()
    driver_wrapper = MobileDriver(appium_driver())
    yield driver_wrapper
    CoreDriver.driver = None


@pytest.fixture
def mocked_selenium_driver():
    selenium_driver = SeleniumDriver
    selenium_driver.__init__ = lambda *args, **kwargs: None
    selenium_driver.session_id = None
    selenium_driver.command_executor = MagicMock()
    selenium_driver.error_handler = MagicMock()

    driver_wrapper = DriverWrapper(selenium_driver())
    yield driver_wrapper
    CoreDriver.driver = None


@pytest.fixture
def mocked_play_driver():
    driver_wrapper = DriverWrapper(Browser(MagicMock()))
    DriverWrapper.driver_wrapper = driver_wrapper
    DriverWrapper.driver = PlaywrightDriver(MagicMock())
    yield driver_wrapper
    PlayDriver.driver = None
