import pytest


def test_driver_opened(selenium_driver):
    assert (selenium_driver.is_driver_opened(), selenium_driver.is_driver_closed()) == (True, False)


@pytest.mark.no_teardown
def test_driver_closed(selenium_driver):
    initial_opened = selenium_driver.is_driver_opened()
    selenium_driver.quit()
    assert all((initial_opened, selenium_driver.is_driver_closed()))
