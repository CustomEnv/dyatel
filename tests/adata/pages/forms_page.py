from dyatel.base.page import Page
from tests.adata.elements.forms_groups import ValidationForm, ControlsForm


class FormsPage(Page):
    def __init__(self):
        self.url = 'https://dineshvelhal.github.io/testautomation-playground/forms.html'
        self.validation_form = ValidationForm()
        self.controls_form = ControlsForm()
        super().__init__('//*[.="Basic Form Controls"]', name='Forms page')
