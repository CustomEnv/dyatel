import os

import pytest

from data_for_testing.pages.sidebar_page import SidebarPage

from data_for_testing.pages.tabs_page import TabsPage
from tests.web_tests.conftest import sidebar_page_path


@pytest.fixture
def opened_sidebar_page(driver):  # New page (based on existing) with opened sidebar at page loading
    sidebar_page_url = sidebar_page_path.replace('file://', '')
    new_file, sidebar_style_matches = [], ('sidebar_style', 'display: none;')

    with open(sidebar_page_url, 'r') as file:
        for row in file.readlines():
            if any(x in row for x in sidebar_style_matches):
                row = row.replace('display: none;', 'display: inline;')
            new_file.append(row)

    sidebar_shown_page_url = sidebar_page_url.replace('sidebar_page', 'sidebar_shown_page')

    with open(sidebar_shown_page_url, 'w') as file:
        file.writelines(new_file)

    driver.get(f'file://{sidebar_shown_page_url}')
    yield SidebarPage()
    os.remove(sidebar_shown_page_url)


def test_sidebar_page_open_sidebar(sidebar_page):
    initial_displayed = sidebar_page.sidebar.is_displayed()
    sidebar_page.sidebar.open_navigation_sidebar()
    after_action_displayed = sidebar_page.sidebar.is_displayed()
    assert (initial_displayed, after_action_displayed) == (False, True)


def test_sidebar_page_close_sidebar(opened_sidebar_page):
    initial_displayed = opened_sidebar_page.sidebar.wait_element().is_displayed()
    opened_sidebar_page.sidebar.close_navigation_sidebar()
    after_action_displayed = opened_sidebar_page.sidebar.is_displayed()
    assert (initial_displayed, after_action_displayed) == (True, False)


def test_sidebar_page_page_title(sidebar_page):
    assert sidebar_page.title.wait_element().get_text == 'SeleniumMaster sidebar page'


def test_sidebar_page_navigation(sidebar_page):
    sidebar_page.sidebar.open_navigation_sidebar()
    sidebar_page.sidebar.navigate_to('tabs-page')
    assert TabsPage().wait_page_loaded()
