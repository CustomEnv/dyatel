from mops.base.element import Element
from mops.base.page import Page


class ProgressBarPage(Page):
    def __init__(self):
        self.url = 'http://uitestingplayground.com/progressbar'
        super().__init__('.progress', name='Progressbar page')

    progress_bar = Element('progressBar', name='progress bar')
    stop_button = Element('stopButton', name='stop button')
    start_button = Element('startButton', name='start button')
