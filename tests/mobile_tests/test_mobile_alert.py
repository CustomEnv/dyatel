def test_dismiss_mobile_alert1(expected_condition_page, driver_wrapper):
    expected_condition_page.prompt_trigger.click()
    driver_wrapper.dismiss_alert()
    assert expected_condition_page.canceled_badge.wait_visibility().is_displayed()


def test_accept_mobile_alert(expected_condition_page, driver_wrapper):
    expected_condition_page.prompt_trigger.click()
    driver_wrapper.accept_alert()
    assert expected_condition_page.confirm_badge.wait_visibility().is_displayed()


def test_dismiss_mobile_alert_native(expected_condition_page, driver_wrapper):
    expected_condition_page.prompt_trigger.click()
    expected_condition_page.alert_cancel_button.click_in_alert()
    assert expected_condition_page.canceled_badge.wait_visibility().is_displayed()


def test_accept_mobile_alert_native(expected_condition_page, driver_wrapper):
    expected_condition_page.prompt_trigger.click()
    expected_condition_page.alert_ok_button.click_in_alert()
    assert expected_condition_page.confirm_badge.wait_visibility().is_displayed()
