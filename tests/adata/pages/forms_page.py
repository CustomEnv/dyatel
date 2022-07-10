from dyatel.base.page import Page
from tests.adata.elements.nested_groups import ValidationForm


class FormsPage(Page):
    def __init__(self):
        self.url = 'https://testautomation-playground.herokuapp.com/forms.html'
        self.validation_form = ValidationForm()
        super().__init__('//*[.="Basic Form Controls"]', name='Forms page')
