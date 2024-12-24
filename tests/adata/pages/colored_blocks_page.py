from typing import List

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page
from tests.settings import domain_name, repo_name


class Row(Group):
    def __init__(self, locator, name: str):
        self.card = Element('.card', name=f'any colored block of {name}')
        super().__init__(locator, name=name)


class ColoredBlocksPage(Page):
    
    def __init__(self):
        super().__init__('colored-blocks-page', name='Colored blocks page')

    url = f'{domain_name}/{repo_name}/colored_blocks.html'

    blocks_container = Element('.container', name='colored blocks container')
    row1 = Row('row-1', name='first blocks row')
    row2 = Row('row-2', name='second blocks row')
    card = Element('.card', name='any colored block')
    navbar = Element('.navbar', name='navbar')

    def get_all_cards(self) -> List[Element]:
        return self.card.all_elements