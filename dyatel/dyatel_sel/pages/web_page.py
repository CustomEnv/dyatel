from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_page import CorePage


class WebPage(CorePage):

    def __init__(self, locator, locator_type=None, name=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        CorePage.__init__(self, locator=locator, locator_type=locator_type, name=name)
