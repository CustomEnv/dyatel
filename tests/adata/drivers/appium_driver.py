from appium.webdriver.webdriver import WebDriver as SourceAppiumDriver

from dyatel.base.driver_wrapper import DriverWrapperSessions
from tests.adata.drivers.driver_entities import DriverEntities
from tests.adata.drivers.selenium_driver import SeleniumDriver
from appium.options.common.base import AppiumOptions
from tests.settings import get_android_desired_caps, ios_desired_caps


class AppiumDriver:

    @staticmethod
    def create_appium_driver(entities: DriverEntities):
        appium_ip = entities.config.getoption('--appium-ip')
        appium_port = entities.config.getoption('--appium-port')
        command_exc = f'http://{appium_ip}:{appium_port}'
        is_android = entities.platform == 'android'

        caps = get_android_desired_caps() if is_android else ios_desired_caps
        caps.update({'browserName': entities.driver_name.title()})

        if is_android:
            caps.update({'chromedriverArgs': ['--hide-scrollbars']})

        if DriverWrapperSessions.is_connected():
            return SeleniumDriver.create_selenium_driver(entities)

        options = AppiumOptions().load_capabilities(caps)

        return SourceAppiumDriver(command_executor=command_exc, options=options)
