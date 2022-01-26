from selenium.webdriver.common.by import By
from selenium_master.elements.web_element import WebElement
from selenium_master.pages.web_page import WebPage

from data_for_testing.components.mixin import Mixin

available_tabs = ('London', 'Paris', 'Tokyo')


class TabsPage(WebPage, Mixin):
    """ Correspond to tabs_page.html """

    def __init__(self):
        super().__init__(By.CSS_SELECTOR, '[data-qa-marker = tabs-page]', name='Tabs page')

    @property
    def page_title(self):
        return WebElement(By.CSS_SELECTOR, '[data-qa-marker = sidebar-page-title]', name='title')

    def tab_with_name(self, name):
        assert name in available_tabs, f'Give expected tab name from {available_tabs}'
        return WebElement(By.XPATH, f'//*[contains(@class, "bar-item") and .="{name}"]', name=f'tab with name "{name}"')

    def tab_title(self, name):
        assert name in available_tabs, f'Give expected tab name from {available_tabs}'
        return WebElement(By.XPATH, f'//h2[.="{name}"]', name=f'tab title with name "{name}"')

    def navigate_to_tab(self, name):
        self.tab_with_name(name).wait_element().click()
        self.tab_title(name).wait_element()
        return self
