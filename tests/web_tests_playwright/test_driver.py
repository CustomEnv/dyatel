import pytest


def test_driver_opened(playwright_driver):
    driver = playwright_driver.driver
    assert driver.is_connected()


@pytest.mark.no_teardown
def test_driver_closed(playwright_driver):
    driver = playwright_driver.driver
    driver.close()
    assert not driver.is_connected()
