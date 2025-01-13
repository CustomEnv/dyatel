def test_element_initialisation_inside_driver_wrapper(mocked_selenium_driver, mocked_ios_driver):
    """
    dummy_element is an object inside DriverWrapper,
      so it can fail on initialisation with 2 drivers due to PreviousObjectDriver process
    """
    assert mocked_selenium_driver.dummy_element()
    assert mocked_ios_driver.dummy_element()
