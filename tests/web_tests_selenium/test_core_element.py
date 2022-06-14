import random

import pytest

from selenium_master.pages.base_page import BasePage
from selenium_master.elements.base_element import BaseElement


class PizzaOrderPage(BasePage):
    def __init__(self):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/order_submit.html'
        super().__init__('//h3[contains(., "Pizza House")]', name='Pizza order page')

    def submit_button(self):
        return BaseElement('submit_button', name='submit order button')

    def error_modal(self):
        return BaseElement('.modal-content', name='error modal popup')

    def quantity_input(self):
        return BaseElement('quantity', name='quantity input')


class PlaygroundHeader(BaseElement):
    def __init__(self):
        super().__init__('.navbar', name='Playground header')

    def nav_button(self, name):
        return BaseElement(f'//a[.="{name}"]', name=f'"{name}" navigation button')

    def navigate_to_resources(self):
        self.nav_button('Resources').click()
        return PlaygroundResourcesPage()

    def navigate_to_home(self):
        self.nav_button('Home').click()
        return PlaygroundMainPage()

    def navigate_to_uitap(self):
        self.nav_button('UITAP').click()
        return PlaygroundMainPage()


class PlaygroundResourcesPage(BasePage):

    def __init__(self):
        self.url = "http://uitestingplayground.com/resources"
        super().__init__('//h3[.="Resources"]', name='Playground resources page')


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


@pytest.fixture
def base_playground_page(driver_wrapper):
    return PlaygroundMainPage().open_page()


@pytest.fixture
def pizza_order_page(driver_wrapper):
    return PizzaOrderPage().open_page()


def test_element_storage(base_playground_page):
    page_element = base_playground_page.kube()
    assert page_element.element == page_element._elements


def test_elements_storage(base_playground_page):
    page_element = base_playground_page.any_link()
    storage_filled = page_element.all_elements == page_element._elements
    assert all((storage_filled, len(page_element._elements) > 1))


def test_element_displayed_positive(base_playground_page):
    assert base_playground_page.kube().is_displayed()


def test_element_displayed_negative(base_playground_page):
    assert not base_playground_page.kube_broken().is_displayed()


def test_parent_element_positive(base_playground_page):
    assert base_playground_page.kube_parent().is_displayed()


def test_parent_element_negative(base_playground_page):
    assert not base_playground_page.kube_broken_parent().is_displayed()


def test_click_and_wait(pizza_order_page):
    pizza_order_page.submit_button().click()
    after_click_displayed = pizza_order_page.error_modal().wait_element().is_displayed()
    pizza_order_page.error_modal().click_outside()
    after_click_outside_not_displayed = not pizza_order_page.error_modal().wait_element_hidden().is_displayed()
    assert all((after_click_displayed, after_click_outside_not_displayed))


def test_wait_without_error(pizza_order_page):
    pizza_order_page.error_modal().wait_element_without_error(timeout=0.01)
    assert not pizza_order_page.error_modal().is_displayed()


@pytest.mark.xfail_platform('android', reason='can not get text from that element')
def test_type_clear_text_get_value(pizza_order_page):
    text_to_send = str(random.randint(100, 9999))
    pizza_order_page.quantity_input().type_text(text_to_send)
    text_added = pizza_order_page.quantity_input().get_value == text_to_send
    pizza_order_page.quantity_input().clear_text()
    text_erased = pizza_order_page.quantity_input().get_value == ''
    assert all((text_added, text_erased))

