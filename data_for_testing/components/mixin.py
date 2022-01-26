from selenium.webdriver.common.by import By
from selenium_master.elements.web_element import WebElement


class Mixin:

    @property
    def cross_button(self):
        return WebElement(By.CSS_SELECTOR, '[data-qa-marker = cross-button]', name='cross button')
