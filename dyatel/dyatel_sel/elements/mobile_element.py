from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement


class MobileElement(CoreElement):

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver: AppiumWebDriver = CoreDriver.driver
        super(MobileElement, self).__init__(locator=locator, locator_type=locator_type, name=name, parent=parent)
