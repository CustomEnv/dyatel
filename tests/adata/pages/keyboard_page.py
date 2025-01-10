from mops.base.element import Element
from mops.base.page import Page
from tests.settings import domain_name, automation_playground_repo_name


class KeyboardPage(Page):
    def __init__(self):
        self.url = f'{domain_name}/{automation_playground_repo_name}/keyboard_events.html'
        super().__init__('//h2[.="Keyboard Actions"]', name='Keyboard actions page')

    input_area = Element('textarea', name='input area')
    key_badge = Element('code', name='pressed key badge')
