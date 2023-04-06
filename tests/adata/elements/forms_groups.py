from dyatel.base.element import Element
from dyatel.base.group import Group


class FormMixin(Group):
    input = Element('input', name='input')  # Cover nested groups issue


class ValidationForm(Group):
    def __init__(self):
        self.form_mixin = FormMixin('.card-body', name='Form mixin')
        super().__init__('//*[contains(@class, "card") and .//.="Form with Validations"]', name='Validation form')

    submit_form_button = Element('button', name='submit form button')
    invalid_city_error = Element('invalid_city', name='invalid city error')
    invalid_feedback_error = Element('invalid_state', name='invalid feedback error')
    invalid_zip_error = Element('invalid_zip', name='invalid zip error')
    invalid_terms_error = Element('invalid_terms', name='invalid terms error')
    any_error = Element('[class *= invalid]', name='any error')


class ControlsForm(Group):
    def __init__(self):
        super().__init__('//*[contains(@class, "card") and .//.="Basic Form Controls"]', name='Controls form')

    python_checkbox = Element('check_python', name='python checkbox')
    selenium_radio = Element('rad_selenium', name='selenium radiobutton')
    protractor_radio = Element('rad_protractor', name='protractor radiobutton')
    german_slider = Element('.custom-control-label', name='german language slider')
