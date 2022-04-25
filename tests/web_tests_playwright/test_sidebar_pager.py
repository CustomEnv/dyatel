import os

import pytest

from data_for_testing.utils import sidebar_page_path
from data_for_testing.web.playwright.pages.sidebar_page import SidebarPagePlaywright
from data_for_testing.web.playwright.pages.tabs_page import TabsPagePlaywright


@pytest.fixture
def opened_sidebar_page(playwright_driver):  # New page (based on existing) with opened sidebar at page loading
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

    page = SidebarPagePlaywright()
    page.get(f'file://{sidebar_shown_page_url}')
    yield page
    os.remove(sidebar_shown_page_url)


def test_sidebar_page_page_title(sidebar_page):
    assert sidebar_page.title.get_text() == 'SeleniumMaster sidebar page'


def test_sidebar_page_open_sidebar(sidebar_page):
    initial_hidden = sidebar_page.sidebar.is_hidden()
    sidebar_page.sidebar.open_navigation_sidebar()
    after_action_displayed = sidebar_page.sidebar.is_displayed()
    assert all((initial_hidden, after_action_displayed))


def test_sidebar_page_close_sidebar(opened_sidebar_page):
    initial_displayed = opened_sidebar_page.sidebar.is_displayed()
    opened_sidebar_page.sidebar.close_navigation_sidebar()
    after_action_hidden = opened_sidebar_page.sidebar.is_hidden()
    assert all((initial_displayed, after_action_hidden))


def test_sidebar_page_navigation(sidebar_page):
    sidebar_page.sidebar.open_navigation_sidebar()
    sidebar_page.sidebar.navigate_to('tabs-page')
    assert TabsPagePlaywright().wait_until_opened()
