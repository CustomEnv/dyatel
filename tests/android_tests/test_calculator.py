from string import ascii_letters, punctuation
from random import randint, getrandbits

import allure
import pytest

from data_for_testing.pages.simple_calculator_page import CalculatorPage


# TODO: Navigation by link in TextView test can be added:
#     https://stackoverflow.com/questions/52256409/how-can-i-click-on-text-link-inside-in-textview-in-appium


@pytest.fixture
def calculator_page(mobile_driver):
    return CalculatorPage().wait_page_loaded()


@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize(
    argnames='case',
    argvalues=(
        {'id': 'zero value', 'a': 0, 'b': 0},
        {'id': 'integers', 'a': randint(1, 100), 'b': randint(1, 100)},
        {'id': 'negative integers', 'a': randint(-100, -1), 'b': randint(-100, 100)},
        pytest.param({'id': 'large integers', 'a': getrandbits(32), 'b': getrandbits(32)},
                     marks=pytest.mark.xfail(reason='Large values not supported. App crashed')),
        pytest.param({'id': 'decimals', 'a': randint(1, 100) / 1, 'b': randint(1, 100) / 1},
                     marks=pytest.mark.xfail(reason='Decimals not supported. App crashed')),
    ),
    ids=lambda param: param['id']
)
def test_calculator_sum(calculator_page, case):
    """ Test sum of two values in simple (only sum) calculator app """
    a_input_text, b_input_text = case['a'], case['b']
    calculator_page.input_a.wait_element().type_text(a_input_text)
    calculator_page.input_b.wait_element().type_text(b_input_text)
    assert calculator_page.input_sum.wait_element().get_text == str(a_input_text + b_input_text)


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    argnames='case',
    argvalues=(
        pytest.param({'id': 'letters', 'text': ascii_letters},
                     marks=pytest.mark.xfail(reason='Driver exception. TODO: Check workaround with press_keycode')),
        pytest.param({'id': 'punctuation', 'text': punctuation},
                     marks=pytest.mark.xfail(reason='Driver exception. TODO: Check workaround with press_keycode')),
    ),
    ids=lambda param: param['id']
)
def test_calculator_input_restriction(mobile_driver, calculator_page, case):
    """ Test restriction of typing invalid characters """
    calculator_page.input_a.wait_element().type_text(case['text'])
    calculator_page.input_b.wait_element().type_text(case['text'])
    assert calculator_page.input_sum.wait_element().get_text == ''


@pytest.mark.xfail(reason='App crashed after clear input text')
@allure.severity(allure.severity_level.CRITICAL)
def test_calculator_clear_input(calculator_page):
    """ Test clearing the inputs """
    calculator_page.input_a.wait_element().type_text(randint(1, 100))
    calculator_page.input_b.wait_element().type_text(randint(1, 100))

    calculator_page.input_a.clear_text()
    calculator_page.input_b.clear_text()

    assert not all((calculator_page.input_a.get_text, calculator_page.input_b.get_text))
