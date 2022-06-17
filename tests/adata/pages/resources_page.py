from selenium_master.base.base_page import BasePage


class PlaygroundResourcesPage(BasePage):

    def __init__(self):
        self.url = "http://uitestingplayground.com/resources"
        super().__init__('//h3[.="Resources"]', name='Playground resources page')
