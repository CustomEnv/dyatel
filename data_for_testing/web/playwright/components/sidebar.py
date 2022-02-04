from playwright_master.web_element import WebElement

from data_for_testing.web.playwright.components.mixin import MixinPlaywright


class SidebarPlaywright(WebElement, MixinPlaywright):

    def __init__(self):
        super().__init__('[data-qa-marker = sidebar]', name='Sidebar')

    @property
    def hamburger_button(self):
        return WebElement('[data-qa-marker = hamburger-button]', name='hamburger button')

    def navigation_item(self, link_text):
        return WebElement(f'[data-qa-marker = {link_text}][data-qa-type = navigation-item]',
                          name=f'{link_text} navigation item')

    def navigate_to(self, page):
        self.navigation_item(page).click()

    def open_navigation_sidebar(self):
        self.hamburger_button.click()
        self.wait_element()
        return self

    def close_navigation_sidebar(self):
        self.cross_button.click()
        self.wait_element_hidden()
        return self
