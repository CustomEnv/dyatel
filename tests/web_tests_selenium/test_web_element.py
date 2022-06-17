def test_hover(mouse_event_page):
    initial_not_displayed = not mouse_event_page.dropdown.is_displayed()
    mouse_event_page.choose_language_button.hover()
    after_hover_displayed = mouse_event_page.dropdown.wait_element_without_error().is_displayed()
    assert all((initial_not_displayed, after_hover_displayed))

