import logging
import os
from subprocess import run

import allure
import pytest
from appium.webdriver.webdriver import WebDriver as AppiumDriver

from allure_commons.types import AttachmentType
from data_for_testing.utils import set_logging_settings
from selenium_master.driver.mobile_driver import MobileDriver


set_logging_settings()


desired_caps = {
    'deviceName': 'iPhone 13',
    'platformName': 'iOS',
    'platformVersion': '15.2',
    'udid': 'A2A7D60B-921F-4EDB-8883-203249E9A6DB',
    'app': f'{os.getcwd()}/data_for_testing/apps/sample_app_ios.zip',
    'bundleId': 'io.appium.IosAppSeleniumMaster',
    'automationName': 'XCUITest',
    'newCommandTimeout': 9000,
    'wdaLaunchTimeout': 120000,
}


def pytest_addoption(parser):
    parser.addoption('--appium-ip', default='0.0.0.0')
    parser.addoption('--appium-port', default='2000')


@pytest.fixture(scope='session')
def stop_emulator():
    yield
    logging.info('Shutdown iOS emulator')
    run('xcrun simctl shutdown all', shell=True, check=True)


@pytest.fixture
def mobile_driver(request, stop_emulator):
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    all_pytest_markers = [marker.name for marker in request.node.own_markers]

    logging.info('Start iOS emulator')
    logging.info('Installing & launching iOS app')
    appium_driver = AppiumDriver(command_executor=command_exc, desired_capabilities=desired_caps)
    mobile_driver = MobileDriver(driver=appium_driver)
    logging.info('iOS app ready')

    request.node.node_driver = mobile_driver
    yield mobile_driver
    if 'no_teardown' not in all_pytest_markers:
        logging.info('Terminate application')
        mobile_driver.terminate_app(desired_caps['bundleId'])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    driver = getattr(item, 'node_driver', None)
    xfail = hasattr(result, 'wasxfail')
    failure = (result.skipped and xfail) or (result.failed and not xfail)

    if failure and item.config.getoption('--alluredir') and call.when != 'setup' and driver:
        screenshot_name = f'screenshot_{item.name}'
        allure.attach(driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=AttachmentType.PNG)
