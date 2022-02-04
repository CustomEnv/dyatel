import time
from logging import info

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium_master.driver.core_driver import CoreDriver


class CoreElement:
    def __init__(self, locator_type=None, locator=None, name=None):
        self.locator_type = locator_type
        self.locator = locator
        self.name = name
        self.driver = CoreDriver.driver
        self.wait = WebDriverWait(self.driver, 10)

    @property
    def element(self):
        return self.driver.find_element(by=self.locator_type, value=self.locator)

    def wait_element(self, silent=False):
        if not silent:
            info(f'Wait until presence of {self.name}')
        self.wait.until(EC.visibility_of_element_located((self.locator_type, self.locator)))
        return self

    def wait_clickable(self, silent=False):
        if not silent:
            info(f'Wait until clickable of {self.name}')
        self.wait.until(EC.element_to_be_clickable((self.locator_type, self.locator)))
        return self

    def type_text(self, text, silent=False):
        if not silent:
            info(f'Type text {text} into {self.name}')
        self.element.send_keys(text)
        return self

    def type_slowly(self, text, sleep_gap=0.05, silent=False):
        if not silent:
            info(f'Type text {text} into {self.name}')
        for letter in text:
            self.element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, silent=False):
        if not silent:
            info(f'Clear text in {self.name}')
        self.element.clear()
        return self

    @property
    def get_text(self):
        info(f'Get text from {self.name}')
        return self.element.text
