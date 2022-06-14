def test_driver_opened(driver_wrapper):
    assert (driver_wrapper.is_driver_opened(), driver_wrapper.is_driver_closed()) == (True, False)
