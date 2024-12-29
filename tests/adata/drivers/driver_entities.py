from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


class DriverEntities:

    def __init__(
            self,
            request,
            driver_name,
            platform,
            selenium_chrome_options: ChromeOptions,
            selenium_firefox_options: FirefoxOptions,
            selenium_safari_options: SafariOptions,
            env: str,
            **kwargs, # noqa
    ):
        self.request = request
        self.driver_name = driver_name
        self.platform = platform
        self.selenium_chrome_options = selenium_chrome_options
        self.selenium_firefox_options = selenium_firefox_options
        self.config = self.request.config
        self.env = env
        self.selenium_safari_options = selenium_safari_options
