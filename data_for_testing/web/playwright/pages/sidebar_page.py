from playwright_master.web_element import WebElement
from playwright_master.web_page import WebPage

from data_for_testing.web.playwright.components.sidebar import SidebarPlaywright


class SidebarPagePlaywright(WebPage):
    """ Correspond to sidebar_page.html """

    def __init__(self):
        self.sidebar = SidebarPlaywright()
        super(SidebarPagePlaywright, self).__init__(locator='[data-qa-marker = sidebar-page]', name='Sidebar page')

    @property
    def title(self):
        return WebElement(locator='[data-qa-marker = sidebar-page-title]', name='page title')
