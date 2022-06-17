from selenium_master.base.base_element import BaseElement
from selenium_master.base.base_page import BasePage


class PizzaOrderPage(BasePage):
    def __init__(self):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/order_submit.html'
        super().__init__('//h3[contains(., "Pizza House")]', name='Pizza order page')

    submit_button = BaseElement('submit_button', name='submit order button')
    error_modal = BaseElement('.modal-content', name='error modal popup')
    quantity_input = BaseElement('quantity', name='quantity input')
