from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class ExpectedConditionPage(Page):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/expected_conditions.html'
        self.wait_value_card = WaitValueCard()
        super().__init__('//*[contains(@class, "card") and contains(., "wait")]', name='Expected condition page')

    min_wait_input = Element('min_wait', name='min wait input')
    max_wait_input = Element('max_wait', name='max wait input')

    def set_min_and_max_wait(self):
        self.min_wait_input.set_text(1)
        self.max_wait_input.set_text(1)
        return self


class WaitValueCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and contains(., "Wait for text")]', name='wait value card')

    wait_for_text_button = Element('wait_for_text', name='wait for text button')
    wait_for_value_input = Element('wait_for_value', name='wait for value input')
    trigger_button = Element('text_value_trigger', name='trigger wait button')
