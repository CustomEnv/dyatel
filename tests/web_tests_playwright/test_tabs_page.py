from random import choice

import pytest

from data_for_testing.utils import available_tabs


@pytest.mark.parametrize('case', available_tabs)
def test_tabs_page_navigation_between_tabs(tabs_page, case):
    tabs_page.navigate_to_tab(case)
    assert tabs_page.tab_title(case).is_displayed()


def test_tabs_page_close_after_navigation(tabs_page):
    random_tab = choice(available_tabs)
    tabs_page.navigate_to_tab(random_tab)
    initial_displayed = tabs_page.tab_title(random_tab).is_displayed()
    tabs_page.cross_button.click().wait_element_hidden()
    after_action_displayed = tabs_page.tab_title(random_tab).is_displayed()
    assert (initial_displayed, after_action_displayed) == (True, False)
