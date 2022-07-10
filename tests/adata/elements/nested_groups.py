from dyatel.base.element import Element
from dyatel.base.group import Group


class FormMixin(Group):
    input = Element('input', name='input')


class ValidationForm(Group):
    def __init__(self):
        self.form_mixin = FormMixin('.card-body', name='Form mixin')
        super().__init__('//*[contains(@class, "card") and .//.="Form with Validations"]', name='Validation Form')

    submit_form_button = Element('button', name='submit form button')
    invalid_city_error = Element('invalid_city', name='invalid city error')
    invalid_feedback_error = Element('invalid_state', name='invalid feedback error')
    invalid_zip_error = Element('invalid_zip', name='invalid zip error')
    invalid_terms_error = Element('invalid_terms', name='invalid terms error')
