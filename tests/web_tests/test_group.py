from tests.adata.pages.mouse_event_page import MouseEventPage


def test_base_group_with_class_var_positive(mouse_event_page):
    mouse_click_card = MouseEventPage().mouse_click_card()
    assert mouse_click_card.click_area.is_displayed()


def test_base_group_with_class_var_negative(mouse_event_page):
    mouse_click_card = MouseEventPage().mouse_click_card()
    assert not mouse_click_card.drag_source.is_displayed()


def test_base_group_with_class_func_positive(mouse_event_page):
    mouse_click_card = MouseEventPage().mouse_click_card()
    assert mouse_click_card.click_area_func().is_displayed()


def test_base_group_with_class_func_negative(mouse_event_page):
    mouse_click_card = MouseEventPage().mouse_click_card()
    assert not mouse_click_card.drag_source_func().is_displayed()
