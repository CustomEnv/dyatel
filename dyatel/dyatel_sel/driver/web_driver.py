from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver


class WebDriver(CoreDriver):

    def __init__(self, driver: SeleniumWebDriver):
        self.web_driver: SeleniumWebDriver = driver
        CoreDriver.driver = self.web_driver
        CoreDriver.mobile = False
        CoreDriver.desktop = True
        CoreDriver.__init__(self, driver=self.web_driver)
