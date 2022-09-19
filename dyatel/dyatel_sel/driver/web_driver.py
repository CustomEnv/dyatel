from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver


class WebDriver(CoreDriver):

    def __init__(self, driver: SeleniumWebDriver):
        """
        Initializing of desktop web driver with selenium

        :param driver: selenium driver to initialize
        """
        super().__init__(driver=driver)
