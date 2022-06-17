from selenium_master.base.base_element import BaseElement
from selenium_master.base.base_page import BasePage


class PlaygroundMainPage(BasePage):

    def __init__(self):
        self.url = "http://uitestingplayground.com/home"
        super().__init__('//h1[.="UI Test AutomationPlayground"]', name='Playground main page')

    description_section = BaseElement('description', name='description section')
    overview_section = BaseElement('overview', name='overview section')
    kube = BaseElement('.img-fluid', name='rubik\'s cube')
    any_link = BaseElement('a', name='any link')
    kube_broken = BaseElement('.img-fluid .not-available', name='rubik\'s cube broken locator')
    kube_parent = BaseElement('.img-fluid', name='kube with parent', parent=description_section)
    kube_broken_parent = BaseElement('.img-fluid', name='kube with broken parent', parent=overview_section)
