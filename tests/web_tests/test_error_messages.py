import pytest

from dyatel.exceptions import *
from dyatel.mixins.objects.size import Size

timeout = 0.5


@pytest.mark.medium
def test_wait_elements_count_error_msg(forms_page):
    forms_page.validation_form.form_mixin.input.type_text('sample')
    forms_page.validation_form.submit_form_button.click()
    try:
        forms_page.validation_form.any_error.wait_elements_count(3, timeout=timeout)
    except UnexpectedElementsCountException as exc:
        assert exc.msg == f'Unexpected elements count of "any error" after {timeout} seconds. ' \
                          f'Actual: 4; Expected: 3.'
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_size_error_msg(forms_page):
    try:
        forms_page.validation_form.wait_for_size(Size(200, 400), timeout=timeout)
    except UnexpectedElementSizeException as exc:
        assert f'Unexpected size for "Validation form" after {timeout} seconds. ' in exc.msg
        assert 'Actual: Size' in exc.msg
        assert 'Expected: Size(width=200, height=400).' in exc.msg
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_disabled_error_msg(forms_page):
    try:
        forms_page.validation_form.wait_disabled(timeout=timeout)
    except TimeoutException as exc:
        assert f'"Validation form" not disabled after {timeout} seconds.' in exc.msg
        assert 'Selector:' in exc.msg
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_enabled_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_enabled(timeout=timeout)
    except TimeoutException as exc:
        assert f'"salary input" not enabled after {timeout} seconds. ' in exc.msg
        assert 'Selector:' in exc.msg
        assert 'Parent selector:' in exc.msg
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_non_empty_text_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_for_text(timeout=timeout)
    except UnexpectedTextException as exc:
        assert exc.msg == f'Text of "salary input" is empty after {timeout} seconds.'
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_non_empty_value_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_for_value(timeout=timeout)
    except UnexpectedValueException as exc:
        assert exc.msg == f'Value of "salary input" is empty after {timeout} seconds.'
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_non_specific_text_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_for_text('some text', timeout=timeout)
    except UnexpectedTextException as exc:
        assert exc.msg == f'Not expected text for "salary input" after {timeout} seconds. ' \
                          f'Actual: ""; Expected: "some text".'
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_non_specific_value_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_for_value('some value', timeout=timeout)
    except UnexpectedValueException as exc:
        assert exc.msg == f'Not expected value for "salary input" after {timeout} seconds. ' \
                          f'Actual: ""; Expected: "some value".'
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_visible_error_msg(forms_page):
    try:
        forms_page.controls_form.broken_input.wait_visibility(timeout=timeout)
    except TimeoutException as exc:
        assert f'"invalid element" not visible after {timeout} seconds.' in exc.msg
        assert 'Selector:' in exc.msg
        assert 'Parent selector:' in exc.msg
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_hidden_error_msg(forms_page):
    try:
        forms_page.controls_form.salary_input.wait_hidden(timeout=timeout)
    except TimeoutException as exc:
        assert f'"salary input" still visible after {timeout} seconds.' in exc.msg
        assert 'Selector:' in exc.msg
        assert 'Parent selector:' in exc.msg
    else:
        raise Exception('Unexpected behaviour')


@pytest.mark.medium
def test_wait_element_available_error_msg(forms_page):
    try:
        forms_page.controls_form.broken_input.wait_availability(timeout=timeout)
    except TimeoutException as exc:
        assert f'"invalid element" not available in DOM after {timeout} seconds.' in exc.msg
        assert 'Selector:' in exc.msg
        assert 'Parent selector:' in exc.msg
    else:
        raise Exception('Unexpected behaviour')
