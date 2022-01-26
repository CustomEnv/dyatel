import pytest


def test_driver_opened(driver):
    assert (driver.is_driver_opened(), driver.is_driver_closed()) == (True, False)  # Negative check also


@pytest.mark.no_teardown
def test_driver_closed(driver):
    initial_opened = driver.is_driver_opened()
    driver.quit()
    assert all((initial_opened, driver.is_driver_closed()))
