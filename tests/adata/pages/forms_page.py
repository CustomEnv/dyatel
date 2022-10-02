from dyatel.base.page import Page
from tests.adata.elements.forms_groups import ValidationForm, ControlsForm
from tests.settings import repo_name, domain_name


class FormsPage(Page):
    def __init__(self):
        self.url = f'{domain_name}/{repo_name}/forms.html'
        self.validation_form = ValidationForm()
        self.controls_form = ControlsForm()
        super().__init__('//*[.="Basic Form Controls"]', name='Forms page')
