# class
#
from tests.adata.pages.playground_main_page import PlaygroundMainPage


def test_base_group(base_playground_page):
    assert PlaygroundMainPage().description_section().cool_quote().is_displayed()
    assert not PlaygroundMainPage().description_section().broken_quote().is_displayed()
