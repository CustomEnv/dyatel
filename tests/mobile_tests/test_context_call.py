def get_context_calls_count(driver_wrapper):
    return str(driver_wrapper.driver.get_log('server')).count('driver.getCurrentContext()')


def test_context_calls_count(pizza_order_page, driver_wrapper):
    count_before = get_context_calls_count(driver_wrapper)

    # that can trigger `driver.context` multiple times
    for i in range(3):
        pizza_order_page.submit_button.is_visible()
        pizza_order_page.submit_button.click()
        pizza_order_page.submit_button.hover()
        pizza_order_page.error_modal.click_into_center()

    count_after = get_context_calls_count(driver_wrapper)

    assert count_after >= 2
    assert count_after <= count_before + 1
