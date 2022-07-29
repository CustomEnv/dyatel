def test_switch_context(driver_wrapper):
    assert driver_wrapper.get_current_context() == driver_wrapper.web_context
    driver_wrapper.switch_to_native()
    assert driver_wrapper.get_current_context() == driver_wrapper.native_context
    driver_wrapper.switch_to_web()
    assert driver_wrapper.get_current_context() == driver_wrapper.web_context
