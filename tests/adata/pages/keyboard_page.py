from dyatel.base.element import Element
from dyatel.base.page import Page
from tests.settings import domain_name, repo_name


class KeyboardPage(Page):
    def __init__(self):
        self.url = f'{domain_name}/{repo_name}/keyboard_events.html'
        super().__init__('//h2[.="Keyboard Actions"]', name='Keyboard actions page')

    input_area = Element('area', name='input area')
    key_badge = Element('code', name='pressed key badge')
