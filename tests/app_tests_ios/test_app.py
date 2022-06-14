from time import sleep

import allure
import pytest


@allure.severity(allure.severity_level.CRITICAL)
def test_app_install(mobile_driver):
    """ Install ios application and check running state """
    assert all((mobile_driver.is_app_installed(), mobile_driver.is_app_in_foreground()))


@pytest.mark.no_teardown
@allure.severity(allure.severity_level.CRITICAL)
def test_app_delete(mobile_driver):
    """ Remove ios application and check deleted state """
    mobile_driver.terminate_app(mobile_driver.bundle_id)
    mobile_driver.remove_app(mobile_driver.bundle_id)
    assert mobile_driver.is_app_deleted()


@pytest.mark.no_teardown
@allure.severity(allure.severity_level.CRITICAL)
def test_app_terminate(mobile_driver):
    """ Terminate(close) ios application and check closed state """
    terminate_success = mobile_driver.terminate_app(mobile_driver.bundle_id)
    assert all((terminate_success, mobile_driver.is_app_closed()))


@allure.severity(allure.severity_level.CRITICAL)
def test_app_background(mobile_driver):
    """ Move ios application into background and check background state """
    mobile_driver.background_app(-1)  # move forever into background
    sleep(1)  # sleep for better stability. TODO: can be replaced with `while` cycle
    assert mobile_driver.is_app_in_background()
