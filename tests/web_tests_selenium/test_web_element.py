import pytest

from selenium_master.elements.base_element import BaseElement
from selenium_master.pages.base_page import BasePage


class MouseEventPage(BasePage):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/mouse_events.html'
        super().__init__('//h2[.="Mouse Click Actions"]', name='Mouse events page')

    def choose_language_button(self):
        return BaseElement('button.dropbtn', name='"Choose language" button')

    def dropdown(self):
        return BaseElement('div.dropdown-content', name='dropdown with languages')


@pytest.fixture
def mouse_event_page(driver_wrapper):
    return MouseEventPage().open_page()


def test_hover(mouse_event_page):
    initial_not_displayed = not mouse_event_page.dropdown().is_displayed()
    mouse_event_page.choose_language_button().hover()
    after_hover_displayed = mouse_event_page.dropdown().wait_element_without_error().is_displayed()
    assert all((initial_not_displayed, after_hover_displayed))

