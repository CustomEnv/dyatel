from selenium_master.base.base_element import BaseElement
from selenium_master.base.base_page import BasePage


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
