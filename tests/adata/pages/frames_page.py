from mops.base.element import Element
from mops.base.page import Page
from tests.settings import domain_name, automation_playground_repo_name


class Frame(Element):

    button = Element('button', name='frame button')


class FramesPage(Page):
    def __init__(self):
        self.url = f'{domain_name}/{automation_playground_repo_name}/frames.html'
        super().__init__('//h1[.="Frames Page"]', name='Frames page')

    frame1 = Frame('frame1', name='frame 1')
    frame2 = Frame('frame2', name='frame 2')
    frame3 = Frame('frame3', name='frame 3')
    frame4 = Frame('frame4', name='frame 4')
