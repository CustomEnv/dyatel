from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.dyatel_sel.pages.mobile_page import MobilePage


class WebPage(CorePage):

    def __init__(self, locator, locator_type=None, name=None):
        self.name = name
        self.locator = locator
        self.locator_type = locator_type
        self.driver: SeleniumWebDriver = CoreDriver.driver
        page = MobilePage if CoreDriver.is_ios or CoreDriver.is_android else WebPage
        super(WebPage, self).__init__(locator=locator, locator_type=locator_type, name=name)
