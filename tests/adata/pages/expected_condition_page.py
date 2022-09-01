from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page


class ExpectedConditionPage(Page):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/expected_conditions.html'
        self.value_card = WaitValueCard()
        self.element_card = WaitElementCard()
        self.frame_card = WaitFrameCard()
        self.test_driver = self.driver_wrapper
        super().__init__('//*[contains(@class, "card") and contains(., "wait")]', name='Expected condition page')
        self.test_driver = self.driver_wrapper

    min_wait_input = Element('min_wait', name='min wait input')
    max_wait_input = Element('max_wait', name='max wait input')

    def set_min_and_max_wait(self, min_wait=1, max_wait=1):
        self.min_wait_input.set_text(min_wait)
        self.max_wait_input.set_text(max_wait)
        return self


class WaitValueCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and contains(., "Wait for text")]', name='value card')

    wait_for_text_button = Element('wait_for_text', name='wait for text button')
    wait_for_value_input = Element('wait_for_value', name='wait for value input')
    trigger_button = Element('text_value_trigger', name='trigger wait button')


class WaitElementCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and contains(., "Wait for element to be visible")]',
                         name='element card')

    trigger_button = Element('visibility_trigger', name='trigger button')
    target_button = Element('visibility_target', name='target button')


class WaitFrameCard(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and contains(., "Wait for frame to be available")]',
                         name='element card')

    trigger_button = Element('wait_for_frame', name='trigger button')
    frame = Element('iframe', name='target iframe')
