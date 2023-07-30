from tests.adata.drivers.playwright_driver import PlaywrightDriver
from tests.adata.drivers.appium_driver import AppiumDriver
from tests.adata.drivers.driver_entities import DriverEntities
from tests.adata.drivers.selenium_driver import SeleniumDriver


class DriverFactory:

    @staticmethod
    def create_driver(entities: DriverEntities):

        is_mobile = entities.platform in ('ios', 'android')

        if is_mobile:
            return AppiumDriver.create_appium_driver(entities)
        elif 'selenium' in entities.platform:
            return SeleniumDriver.create_selenium_driver(entities)
        elif 'playwright' in entities.platform:
            return PlaywrightDriver.create_playwright_driver(entities)
        else:
            raise ValueError(f"Unsupported platform: {entities.platform}")


