from dyatel.base.element import Element
from dyatel.base.page import Page


class PlaygroundMainPage(Page):

    def __init__(self):
        self.url = "http://uitestingplayground.com/home"
        super().__init__('//h1[.="UI Test AutomationPlayground"]', name='Playground main page')

    description_section = Element('description', name='description section')
    overview_section = Element('overview', name='overview section')
    overview_section_broken = Element('overviewshka', name='broken overview section')
    kube = Element('.img-fluid', name='rubik\'s cube')
    any_link = Element('a', name='any link')
    kube_broken = Element('.img-fluid .not-available', name='rubik\'s cube broken locator')
    kube_parent = Element('.img-fluid', name='kube with parent', parent=description_section)
    kube_wrong_parent = Element('.img-fluid', name='kube with wrong parent', parent=overview_section)
    kube_broken_parent = Element('.img-fluid', name='kube with broken parent', parent=overview_section_broken)
