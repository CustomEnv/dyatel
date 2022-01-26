from selenium_master.driver.core_driver import CoreDriver
from selenium_master.pages.core_page import CorePage


class WebPage(CorePage):

    def __init__(self, locator_type, locator, name):
        self.driver = CoreDriver.driver
        self.locator_type = locator_type
        self.locator = locator
        self.name = name
        super(WebPage, self).__init__(locator_type, locator, name)

    def wait_page_loaded(self):
        self.wait_page()
        return self
