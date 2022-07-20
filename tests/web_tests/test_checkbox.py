# Checkbox tests


def test_checkbox_check(forms_page):
    initial_not_checked = not forms_page.controls_form.python_checkbox.is_checked()
    forms_page.controls_form.python_checkbox.check()
    after_check_checked = forms_page.controls_form.python_checkbox.is_checked()
    assert all((initial_not_checked, after_check_checked))


def test_checkbox_uncheck(forms_page):
    forms_page.controls_form.python_checkbox.check()
    after_check_checked = forms_page.controls_form.python_checkbox.is_checked()
    forms_page.controls_form.python_checkbox.uncheck()
    after_uncheck_not_checked = not forms_page.controls_form.python_checkbox.is_checked()
    assert all((after_check_checked, after_uncheck_not_checked))


def test_checkbox_value(forms_page):
    assert forms_page.controls_form.python_checkbox.get_text == 'PYTHON'


# Radiobutton tests


def test_radio_check(forms_page):
    initial_not_checked = not forms_page.controls_form.selenium_radio.is_checked()
    forms_page.controls_form.selenium_radio.check()
    after_check_checked = forms_page.controls_form.selenium_radio.is_checked()
    assert all((initial_not_checked, after_check_checked))


def test_radio_uncheck(forms_page):
    forms_page.controls_form.selenium_radio.check()
    after_check_checked = forms_page.controls_form.selenium_radio.is_checked()
    forms_page.controls_form.protractor_radio.check()
    after_uncheck_not_checked = not forms_page.controls_form.selenium_radio.is_checked()
    assert all((after_check_checked, after_uncheck_not_checked))


def test_radio_value(forms_page):
    assert forms_page.controls_form.selenium_radio.get_text == 'SELENIUM'


# Slider tests


def test_slider_check(forms_page):
    initial_not_checked = not forms_page.controls_form.german_slider.is_checked()
    forms_page.controls_form.german_slider.check()
    after_check_checked = forms_page.controls_form.german_slider.is_checked()
    assert all((initial_not_checked, after_check_checked))


def test_slider_uncheck(forms_page):
    forms_page.controls_form.german_slider.check()
    after_check_checked = forms_page.controls_form.german_slider.is_checked()
    forms_page.controls_form.german_slider.uncheck()
    after_uncheck_not_checked = not forms_page.controls_form.german_slider.is_checked()
    assert all((after_check_checked, after_uncheck_not_checked))


def test_slider_value(forms_page):
    assert forms_page.controls_form.german_slider.get_text == 'Speaks German?'
