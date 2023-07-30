from appium.webdriver.webdriver import WebDriver as SourceAppiumDriver

from dyatel.base.driver_wrapper import DriverWrapper
from tests.adata.drivers.driver_entities import DriverEntities
from tests.adata.drivers.selenium_driver import SeleniumDriver
from tests.settings import android_desired_caps, ios_desired_caps


class AppiumDriver:

    @staticmethod
    def create_appium_driver(entities: DriverEntities):
        appium_ip = entities.config.getoption('--appium-ip')
        appium_port = entities.config.getoption('--appium-port')
        command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
        is_android = entities.platform == 'android'

        caps = android_desired_caps if is_android else ios_desired_caps
        caps.update({'browserName': entities.driver_name.title()})

        if is_android:
            caps.update({'chromedriverArgs': ['--hide-scrollbars']})

        if DriverWrapper.driver:
            return SeleniumDriver.create_selenium_driver(entities)

        return SourceAppiumDriver(command_executor=command_exc, desired_capabilities=caps)
