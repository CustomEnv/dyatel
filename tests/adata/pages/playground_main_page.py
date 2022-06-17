from selenium_master.base.base_element import BaseElement
from selenium_master.base.base_group import Group
from selenium_master.base.base_page import BasePage


class PlaygroundMainPage(BasePage):

    def __init__(self):
        self.url = "http://uitestingplayground.com/home"
        super().__init__('//h1[.="UI Test AutomationPlayground"]', name='Playground main page')

    def description_section(self):
        return BaseElement('description', name='description section')

    def overview_section(self):
        return BaseElement('overview', name='overview section')

    def kube(self):
        return BaseElement('.img-fluid', name='rubik\'s cube')

    def any_link(self):
        return BaseElement('a', name='any link')

    def kube_broken(self):
        return BaseElement('.img-fluid .not-available', name='rubik\'s cube broken locator')

    def kube_parent(self):
        return BaseElement('.img-fluid', name='kube with parent', parent=self.description_section())

    def kube_broken_parent(self):
        return BaseElement('.img-fluid', name='kube with broken parent', parent=self.overview_section())
