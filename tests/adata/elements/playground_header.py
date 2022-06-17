from selenium_master.base.base_element import BaseElement
from tests.adata.pages.playground_main_page import PlaygroundMainPage
from tests.adata.pages.resources_page import PlaygroundResourcesPage


class PlaygroundHeader(BaseElement):
    def __init__(self):
        super().__init__('.navbar', name='Playground header')

    def nav_button(self, name):
        return BaseElement(f'//a[.="{name}"]', name=f'"{name}" navigation button')

    def navigate_to_resources(self):
        self.nav_button('Resources').click()
        return PlaygroundResourcesPage()

    def navigate_to_home(self):
        self.nav_button('Home').click()
        return PlaygroundMainPage()

    def navigate_to_uitap(self):
        self.nav_button('UITAP').click()
        return PlaygroundMainPage()
