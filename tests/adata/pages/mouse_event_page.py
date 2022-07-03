from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class MouseEventPage(Page):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/mouse_events.html'
        super().__init__('//h2[.="Mouse Click Actions"]', name='Mouse events page')

    choose_language_button = Element('button.dropbtn', name='"Choose language" button', wait=True)
    dropdown = Element('div.dropdown-content', name='dropdown with languages')
    header_logo = Element('[class = "navbar-brand abs"]', name='header logo', wait=True)

    def mouse_click_card(self):
        return MouseClickCard()


class MouseEventPageWithUnexpectedWait(MouseEventPage):
    dropdown = Element('div.dropdown-content', name='dropdown with languages and wait', wait=True)


class MouseClickCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and .//.="Mouse Click Actions"]', name='mouse click card')

    click_area = Element('click_area', name='click area')
    drag_source = Element('drag_source', name='drag source button')  # Wrong one

    def click_area_func(self):
        return self.click_area

    def drag_source_func(self):
        return self.drag_source  # Wrong one
