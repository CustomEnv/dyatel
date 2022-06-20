from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.dyatel_sel.pages.mobile_page import MobilePage


class WebPage(CorePage):

    def __init__(self, locator, locator_type=None, name=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        super(WebPage, self).__init__(locator=locator, locator_type=locator_type, name=name)
