from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as GeckoWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

from dyatel.base.driver_wrapper import DriverWrapperSessions
from dyatel.mixins.objects.driver import Driver
from tests.adata.drivers.driver_entities import DriverEntities


class SeleniumDriver:

    @staticmethod
    def create_selenium_driver(entities: DriverEntities) -> Driver:
        driver_name = entities.driver_name
        if driver_name == 'safari' and DriverWrapperSessions.is_connected():
            driver_name = 'chrome'  # Cannot create second selenium driver

        if driver_name == 'chrome':
            driver = ChromeWebDriver(options=entities.selenium_chrome_options, service=ChromeService())
        elif driver_name == 'firefox':
            driver = GeckoWebDriver(options=entities.selenium_firefox_options, service=FirefoxService())
        elif driver_name == 'safari':
            driver = SafariWebDriver(service=SafariService())
        else:
            raise ValueError(f"Unsupported driver for selenium: {driver_name}")

        driver.set_window_position(0, 0)  # FIXME

        return Driver(driver=driver)
