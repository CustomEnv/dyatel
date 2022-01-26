from logging import info

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_master.driver.core_driver import CoreDriver


class CorePage:
    def __init__(self, locator_type=None, locator=None, name=None):
        self.locator_type = locator_type
        self.locator = locator
        self.name = name
        self.driver = CoreDriver.driver
        self.wait = WebDriverWait(self.driver, 10)

    def wait_page(self, silent=False):
        if not silent:
            info(f'Wait presence of {self.name}')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self
