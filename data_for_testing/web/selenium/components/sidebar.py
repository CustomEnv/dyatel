from selenium.webdriver.common.by import By
from selenium_master.elements.web_element import WebElement

from data_for_testing.web.selenium.components.mixin import MixinSelenium


class SidebarSelenium(WebElement, MixinSelenium):

    def __init__(self):
        super().__init__(By.CSS_SELECTOR, '[data-qa-marker = sidebar]', name='Sidebar')

    def navigation_item(self, link_text):
        return WebElement(By.CSS_SELECTOR, f'[data-qa-marker = {link_text}][data-qa-type = navigation-item]',
                          name=f'{link_text} navigation item')

    @property
    def hamburger_button(self):
        return WebElement(By.CSS_SELECTOR, '[data-qa-marker = hamburger-button]', name='hamburger button')

    def navigate_to(self, page):
        self.navigation_item(page).wait_element().click()

    def open_navigation_sidebar(self):
        self.hamburger_button.click()
        self.wait_element()
        return self

    def close_navigation_sidebar(self):
        self.cross_button.click()
        self.wait_element_hidden()
        return self
