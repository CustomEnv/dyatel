from dyatel.base.page import Page


class PlaygroundResourcesPage(Page):

    def __init__(self):
        self.url = "http://uitestingplayground.com/resources"
        super().__init__('//h3[.="Resources"]', name='Playground resources page')
