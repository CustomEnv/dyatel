from data_for_testing.utils import available_tabs
from playwright_master.web_element import WebElement
from playwright_master.web_page import WebPage

from data_for_testing.web.playwright.components.mixin import MixinPlaywright


class TabsPagePlaywright(WebPage, MixinPlaywright):
    """ Correspond to tabs_page.html """

    def __init__(self):
        super().__init__('[data-qa-marker = tabs-page]', name='Tabs page')

    @property
    def page_title(self):
        return WebElement('[data-qa-marker = sidebar-page-title]', name='title')

    def tab_with_name(self, name):
        assert name in available_tabs, f'Give expected tab name from {available_tabs}'
        return WebElement(f'//*[contains(@class, "bar-item") and .="{name}"]', name=f'tab with name "{name}"')

    def tab_title(self, name):
        assert name in available_tabs, f'Give expected tab name from {available_tabs}'
        return WebElement(f'//h2[.="{name}"]', name=f'tab title with name "{name}"')

    def navigate_to_tab(self, name):
        self.tab_with_name(name).click()
        self.tab_title(name).wait_element()
        return self
