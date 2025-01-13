from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as GeckoWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.webdriver.remote.webdriver import WebDriver as Remote

from mops.base.driver_wrapper import DriverWrapperSessions
from mops.mixins.objects.driver import Driver
from tests.adata.drivers.driver_entities import DriverEntities


class SeleniumDriver:

    @staticmethod
    def create_selenium_driver(entities: DriverEntities) -> Driver:
        driver_name = entities.driver_name
        options = None
        remote_url = "http://127.0.0.1:4444"

        if driver_name == 'safari':
            if DriverWrapperSessions.is_connected():
                driver_name = 'chrome'  # Cannot create second selenium driver
        elif driver_name == 'chrome':
            options = entities.selenium_chrome_options
        elif driver_name == 'firefox':
            options = entities.selenium_firefox_options
            remote_url += '/wd/hub'
        else:
            raise Exception('Unknown driver: %s' % driver_name)

        if entities.env == 'remote':
            driver = Remote(remote_url, options=options)
        elif driver_name == 'chrome':
            driver = ChromeWebDriver(options=options, service=ChromeService())
        elif driver_name == 'firefox':
            driver = GeckoWebDriver(options=options, service=FirefoxService())
        elif driver_name == 'safari':
            driver = SafariWebDriver(options=entities.selenium_safari_options, service=SafariService())
        else:
            raise ValueError(f"Unsupported driver for selenium: {driver_name}")

        driver.set_window_position(0, 0)  # FIXME

        return Driver(driver=driver)
