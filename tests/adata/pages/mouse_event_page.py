from __future__ import annotations

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class MouseEventPage(Page):
    def __init__(self, driver_wrapper=None):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/mouse_events.html'
        super().__init__('//h2[.="Mouse Click Actions"]', name='Mouse events page', driver_wrapper=driver_wrapper)

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
    click_area_parent = Element('//*[@id="click_area"]/..', name='click area')
    x_result = Element('click_x', name='x result')
    y_result = Element('click_y', name='y result')

    drag_source = Element('drag_source', name='drag source button')  # Wrong one

    def get_result_coordinates(self):
        return [int(element.text.split(' ')[1]) for element in (self.x_result, self.y_result)]

    def get_click_area_middle(self):
        el_rect = self.click_area.get_rect()
        height, width = int(el_rect['height'] / 2), int(el_rect['width'] / 2)
        return [range(side - 1, side + 1) for side in [width, height]]

    def is_click_proceeded(self):
        return self.x_result.is_displayed() or self.y_result.is_displayed()

    def click_area_func(self):
        return self.click_area

    def drag_source_func(self):
        return self.drag_source  # Wrong one
