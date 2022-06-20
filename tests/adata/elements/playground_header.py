from dyatel.base.element import Element
from tests.adata.pages.playground_main_page import PlaygroundMainPage
from tests.adata.pages.resources_page import PlaygroundResourcesPage


class PlaygroundHeader(Element):
    def __init__(self):
        super().__init__('.navbar', name='Playground header')

    def nav_button(self, name):
        return Element(f'//a[.="{name}"]', name=f'"{name}" navigation button')

    def navigate_to_resources(self):
        self.nav_button('Resources').click()
        return PlaygroundResourcesPage()

    def navigate_to_home(self):
        self.nav_button('Home').click()
        return PlaygroundMainPage()

    def navigate_to_uitap(self):
        self.nav_button('UITAP').click()
        return PlaygroundMainPage()
