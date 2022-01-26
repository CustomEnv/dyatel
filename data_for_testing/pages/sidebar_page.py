from selenium.webdriver.common.by import By
from selenium_master.elements.web_element import WebElement
from selenium_master.pages.web_page import WebPage

from data_for_testing.components.sidebar import Sidebar


class SidebarPage(WebPage):
    """ Correspond to sidebar_page.html """

    def __init__(self):
        self.sidebar = Sidebar()
        super().__init__(By.CSS_SELECTOR, '[data-qa-marker = sidebar-page]', name='Sidebar page')

    @property
    def title(self):
        return WebElement(By.CSS_SELECTOR, '[data-qa-marker = sidebar-page-title]', name='title')
