import pytest
from dyatel.mixins.objects.size import Size


@pytest.mark.medium
def test_wait_elements_count_log_msg(forms_page, caplog):
    forms_page.validation_form.wait_elements_count(2)
    assert 'Wait for elements count of "Validation form"' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_size_log_msg(forms_page, caplog):
    forms_page.validation_form.wait_for_size(Size(930, 257))
    assert 'Wait for size of "Validation form"' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_enabled_log_msg(forms_page, caplog):
    forms_page.validation_form.wait_enabled()
    assert 'Wait until "Validation form" becomes enabled' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_disabled_log_msg(forms_page, caplog):
    forms_page.controls_form.salary_input.wait_disabled()
    assert 'Wait until "salary input" becomes disabled' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_visible_log_msg(forms_page, caplog):
    forms_page.validation_form.wait_visibility()
    assert 'Wait for visibility of "Validation form"' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_hidden_log_msg(forms_page, caplog):
    forms_page.controls_form.broken_input.wait_hidden()
    assert 'Wait until "invalid element" becomes hidden' in caplog.messages[0]

@pytest.mark.medium
@pytest.mark.parametrize('case', [None, 'PYTHON'], ids=['any value', 'actual value'])
def test_wait_element_value_log_msg(forms_page, caplog, case):
    forms_page.controls_form.python_checkbox.wait_for_value(case)
    assert 'Wait for value of "python checkbox"' in caplog.messages[0]

@pytest.mark.medium
@pytest.mark.parametrize('case', [None, 'Speaks German?'], ids=['any value', 'actual value'])
def test_wait_element_text_log_msg(forms_page, caplog, case):
    forms_page.controls_form.german_slider.wait_for_text()
    assert 'Wait for text of "german language slider"' in caplog.messages[0]

