import logging
from subprocess import run, Popen

import pytest
import allure
from allure_commons.types import AttachmentType
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium_master.driver.mobile_driver import MobileDriver

from data_for_testing.utils import set_logging_settings


set_logging_settings()


AVD_NAME = 'Pixel3'  # TODO: Change to default "Pixel" value or other. Or avd creation can be integrated


desired_caps = {
    'avd': AVD_NAME,
    'deviceName': AVD_NAME,
    'platformName': 'Android',
    'platformVersion': '11.0',
    'app': 'https://testingbot.com/appium/sample.apk',
    'automationName': 'UiAutomator2',
    'noReset': True,
    'newCommandTimeout': 9000,
    'avdLaunchTimeout': 120000,
    'avdReadyTimeout': 120000,
    'adbExecTimeout': 120000,
}


def pytest_addoption(parser):
    parser.addoption('--appium-ip', default='0.0.0.0')
    parser.addoption('--appium-port', default='1000')


@pytest.fixture(scope='session')
def appium(request):
    """ Programmatically start appium. TODO: Not used at this time """
    # TODO: There an error with available of emulator after killing him at previous session
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    service = AppiumService()

    logging.info('Starting appium server')
    service.start(
        args=[
            '-a', appium_ip,
            '-p', appium_port,
        ]
    )
    assert service.is_running, 'Appium service isn\'t running'
    return service


@pytest.fixture(scope='session')
def stop_appium(appium):
    """ Programmatically stop appium. TODO: Not used at this time """
    yield
    logging.info('Stop Appium server')
    appium.stop()
    assert not appium.is_running, 'Appium service isn\'t stopped'


@pytest.fixture(scope='session')
def emulator():
    """ Programmatically start emulator. TODO: Not used at this time """
    device_name = desired_caps['deviceName']
    logging.info(f'Start emulator {device_name}')
    process = Popen(f'emulator -avd {device_name}', shell=True, close_fds=True)
    return process


@pytest.fixture(scope='session')
def stop_emulator():
    yield
    serial_number = run('adb get-serialno', shell=True, capture_output=True).stdout
    if serial_number:
        serial_number = serial_number.decode('utf8').replace('\n', '')
        logging.info(f'Shutdown emulator {serial_number}')
        assert run(f'adb -s {serial_number} emu kill', shell=True, check=True).returncode == 0


@pytest.fixture
def mobile_driver(request, stop_emulator):
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    all_pytest_markers = [marker.name for marker in request.node.own_markers]

    logging.info(f'Start emulator {AVD_NAME}')
    logging.info('Installing & launching android app')
    appium_driver = AppiumDriver(command_executor=command_exc, desired_capabilities=desired_caps)
    mobile_driver = MobileDriver(driver=appium_driver)
    logging.info('Android app ready')

    request.node.node_driver = mobile_driver
    yield mobile_driver
    if 'no_teardown' not in all_pytest_markers:
        mobile_driver.terminate_app(mobile_driver.desired_capabilities['appPackage'])


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
