from dyatel.base.element import Element
from dyatel.base.page import Page
from tests.settings import domain_name, repo_name


class PizzaOrderPage(Page):
    def __init__(self, driver_wrapper=None):
        self.url = f'{domain_name}/{repo_name}/order_submit.html'
        super().__init__('//h3[contains(., "Pizza House")]', name='Pizza order page', driver_wrapper=driver_wrapper)

    submit_button = Element('submit_button', name='submit order button')
    error_modal = Element('.show .modal-dialog .modal-content', name='error modal popup')
    quantity_input = Element('quantity', name='quantity input')

    def input_with_value(self, value):
        return Element(f'input[value="{value}"]', name=f'input with value: {value}')
