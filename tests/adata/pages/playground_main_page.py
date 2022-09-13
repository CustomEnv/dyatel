from __future__ import annotations

from typing import List

from selenium.webdriver.common.by import By

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class PlaygroundMainPage(Page):

    def __init__(self):
        self.url = "http://uitestingplayground.com/home"
        self.any_div_with_parent = Element('div', name='any div inside page locator', parent=self)
        super().__init__('//*[contains(@class, "container") and .//.="UI Test AutomationPlayground"]',
                         name='Playground main page')

    description_section = Element('description', name='description section')
    overview_section = Element('overview', name='overview section')
    overview_section_broken = Element('overviewshka', name='broken overview section')
    kube = Element('.img-fluid', name='rubik\'s cube')
    any_link = Element('a', name='any link')
    kube_invalid_locator = Element('.img-fluid', locator_type=By.XPATH, name='rubik\'s cube with invalid locator')
    kube_broken = Element('.img-fluid .not-available', name='rubik\'s cube broken locator')
    kube_parent = Element('.img-fluid', name='kube with parent', parent=description_section)
    kube_wrong_parent = Element('.img-fluid', name='kube with wrong parent', parent=overview_section)
    kube_broken_parent = Element('.img-fluid', name='kube with broken parent', parent=overview_section_broken)
    inner_text_1 = Element('//*[@class="row"][2]//*[@class="col-sm"][2]', name='text block 1 for removal')
    inner_text_2 = Element('//*[@class="row"][3]//*[@class="col-sm"][3]', name='text block 2 for removal')
    text_container = Element('#overview .container', name='container of text')
    

class SecondPlaygroundMainPage(Page):
    def __init__(self):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/index.html'
        super(SecondPlaygroundMainPage, self).__init__('//h1[.="The Playground"]', name='Second playground main page')

    def get_all_cards(self) -> List[Card]:
        return Card().all_elements


class Card(Group):
    def __init__(self):
        super(Card, self).__init__('.card', name='action cards')

    button = Element('a', name='proceed card button')
