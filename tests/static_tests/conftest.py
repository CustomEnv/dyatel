import pytest
from mock.mock import MagicMock

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver


@pytest.fixture
def mocked_mobile_driver():
    driver = MagicMock()
    driver.capabilities = MagicMock(return_value={
        'platformName': 'ios', 'browserName': 'safari', 'automationName': 'safari'
    })()
    yield MobileDriver(driver)
    CoreDriver.driver = None


@pytest.fixture
def mocked_selenium_driver():
    yield WebDriver(MagicMock())
    CoreDriver.driver = None


@pytest.fixture
def mocked_play_driver():
    yield PlayDriver(MagicMock())
    PlayDriver.driver = None
