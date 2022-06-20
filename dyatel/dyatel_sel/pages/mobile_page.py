from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_page import CorePage


class MobilePage(CorePage):

    def __init__(self, locator, locator_type=None, name=None):
        self.driver: AppiumWebDriver = CoreDriver.driver
        super(MobilePage, self).__init__(locator=locator, locator_type=locator_type, name=name)
