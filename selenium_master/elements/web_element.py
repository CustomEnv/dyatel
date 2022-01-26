from logging import info

from selenium.webdriver.support import expected_conditions as EC

from selenium_master.driver.core_driver import CoreDriver
from selenium_master.elements.core_element import CoreElement


class WebElement(CoreElement):
    def __init__(self, locator_type, locator, name):
        self.driver = CoreDriver.driver
        self.locator_type = locator_type
        self.locator = locator
        self.name = name
        super(WebElement, self).__init__(locator_type, locator, name)

    def click(self):
        info(f'Click into {self.name}')
        self.wait_element(silent=True).element.click()
        return self

    def is_displayed(self):
        info(f'Check visibility of {self.name}')
        return self.element.is_displayed()

    def wait_element_hidden(self, silent=False):
        if not silent:
            info(f'Wait hidden of {self.name}')
        self.wait.until_not(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self
