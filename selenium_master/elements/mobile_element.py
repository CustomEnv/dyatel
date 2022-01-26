from selenium_master.driver.core_driver import CoreDriver
from selenium_master.elements.core_element import CoreElement


class MobileElement(CoreElement):
    def __init__(self, locator_type, locator, name):
        self.driver = CoreDriver.driver
        self.locator_type = locator_type
        self.locator = locator
        self.name = name
        super(MobileElement, self).__init__(locator_type, locator, name)
