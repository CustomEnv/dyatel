from dyatel.base.element import Element
from dyatel.base.page import Page


class PizzaOrderPage(Page):
    def __init__(self):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/order_submit.html'
        super().__init__('//h3[contains(., "Pizza House")]', name='Pizza order page')

    submit_button = Element('submit_button', name='submit order button')
    error_modal = Element('.modal-content', name='error modal popup')
    quantity_input = Element('quantity', name='quantity input')
