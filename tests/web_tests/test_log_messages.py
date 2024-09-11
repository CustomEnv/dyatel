import pytest
from dyatel.mixins.objects.size import Size


@pytest.mark.medium
def test_wait_element_size_log_msg(forms_page, caplog, driver_wrapper):
    expected_height = 256.5 if driver_wrapper.is_playwright else 257
    expected_width = 930
    forms_page.validation_form.wait_for_size(Size(expected_width, expected_height))
    assert (f'Wait until "Validation form" size will be equal to Size(width={expected_width}, height={expected_height})'
            in caplog.messages[0])


@pytest.mark.medium
def test_wait_elements_count_log_msg(forms_page, caplog):
    forms_page.validation_form.wait_elements_count(2)
    assert 'Wait until elements count of "Validation form" will be equal to "2"' in caplog.messages[0]

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
    assert 'Wait until "Validation form" becomes visible' in caplog.messages[0]

@pytest.mark.medium
def test_wait_element_hidden_log_msg(forms_page, caplog):
    forms_page.controls_form.broken_input.wait_hidden()
    assert 'Wait until "invalid element" becomes hidden' in caplog.messages[0]

@pytest.mark.medium
@pytest.mark.parametrize('case', [None, 'PYTHON'], ids=['any value', 'actual value'])
def test_wait_element_value_log_msg(forms_page, caplog, case):
    forms_page.controls_form.python_checkbox.wait_for_value(case)
    if case:
        assert 'Wait until value of "python checkbox" will be equal to "PYTHON"' in caplog.messages[0]
    else:
        assert 'Wait for any value inside "python checkbox"' in caplog.messages[0]

@pytest.mark.medium
@pytest.mark.parametrize('case', [None, 'Speaks German?'], ids=['any value', 'actual value'])
def test_wait_element_text_log_msg(forms_page, caplog, case):
    forms_page.controls_form.german_slider.wait_for_text(case)
    if case:
        assert 'Wait until text of "german language slider" will be equal to "Speaks German?"' in caplog.messages[0]
    else:
        assert 'Wait for any text of "german language slider"' in caplog.messages[0]


@pytest.mark.medium
def test_wait_visibility_log_msg(forms_page, caplog):
    forms_page.controls_form.german_slider.wait_visibility()
    assert 'Wait until "german language slider" becomes visible' in caplog.messages[0]

@pytest.mark.medium
def test_wait_hidden_log_msg(forms_page, caplog):
    forms_page.controls_form.broken_input.wait_hidden()
    assert 'Wait until "invalid element" becomes hidden' in caplog.messages[0]


@pytest.mark.medium
def test_wait_availability_log_msg(forms_page, caplog):
    forms_page.controls_form.german_slider.wait_availability()
    assert 'Wait until presence of "german language slider"' in caplog.messages[0]


