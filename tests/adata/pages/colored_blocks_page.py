from typing import List

from dyatel.base.element import Element
from dyatel.base.page import Page
from tests.settings import domain_name, repo_name


class ColoredBlocksPage(Page):
    
    def __init__(self):
        super().__init__('colored-blocks-page', name='Colored blocks page')

    url = f'{domain_name}/{repo_name}/colored_blocks.html'

    blocks_container = Element('.container', name='colored blocks container')
    card = Element('.card', name='any colored block')
    navbar = Element('.navbar', name='navbar')

    def get_all_cards(self) -> List[Element]:
        return self.card.all_elements