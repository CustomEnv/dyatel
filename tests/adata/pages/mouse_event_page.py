from selenium_master.base.base_element import BaseElement
from selenium_master.base.base_group import Group
from selenium_master.base.base_page import BasePage


class MouseEventPage(BasePage):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/mouse_events.html'
        super().__init__('//h2[.="Mouse Click Actions"]', name='Mouse events page')

    def choose_language_button(self):
        return BaseElement('button.dropbtn', name='"Choose language" button')

    def dropdown(self):
        return BaseElement('div.dropdown-content', name='dropdown with languages')

    def mouse_click_card(self):
        return MouseClickCard()


class MouseClickCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and .//.="Mouse Click Actions"]', name='mouse click card')

    click_area = BaseElement('click_area', name='click area')

    drag_source = BaseElement('drag_source', name='drag source button')  # Wrong one

    def click_area_func(self):
        return self.click_area

    def drag_source_func(self):
        return self.drag_source  # Wrong one
