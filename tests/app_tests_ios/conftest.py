import logging

import allure
import pytest
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from appium.webdriver.appium_service import AppiumService
from allure_commons.types import AttachmentType

from tests.settings import ios_desired_caps
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.shared_utils import set_logging_settings, resize_image, shell_running_command, shell_command


set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--appium-ip', default='0.0.0.0')
    parser.addoption('--appium-port', default='2000')


@pytest.fixture(scope='session')
def appium(request):
    """ Programmatically start and stop appium. Not used at this time """
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    service = AppiumService()

    logging.info('Starting appium server')
    process = service.start(
        args=[
            '-a', appium_ip,
            '-p', appium_port,
            '-g', '.tox/.tmp/logs/ios_appium.txt'
        ],
        timeout_ms=5000,
    )
    assert service.is_running, 'Appium service isn\'t running'
    yield process
    logging.info('Stop Appium server')
    service.stop()
    assert not service.is_running, 'Appium service isn\'t stopped'


@pytest.fixture(scope='session')
def emulator():
    """ Programmatically start and stop emulator """
    device_name, device_udid = ios_desired_caps['deviceName'], ios_desired_caps['udid']
    logging.info(f'Starting simulator {device_name}')
    process = shell_running_command(f'xcrun simctl boot {device_udid}')
    yield process

    if device_udid:
        logging.info('Shutdown iOS emulator')
        assert shell_command(f'xcrun simctl shutdown {device_udid}', check=True).is_success

    if process.pid:
        logging.info(f'Kill simulator process by pid "{process.pid}"')
        assert shell_command(f'kill -9 {process.pid}', check=True).is_success


@pytest.fixture
def mobile_driver(request, emulator):
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    all_pytest_markers = [marker.name for marker in request.node.own_markers]

    logging.info('Installing & launching iOS app')
    appium_driver = AppiumDriver(command_executor=command_exc, desired_capabilities=ios_desired_caps)
    mobile_driver = MobileDriver(driver=appium_driver)
    logging.info('iOS app ready')

    request.node.node_driver = mobile_driver
    yield mobile_driver
    if 'no_teardown' not in all_pytest_markers:
        logging.info('Terminate application')
        mobile_driver.terminate_app(ios_desired_caps['bundleId'])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Generate report """
    outcome = yield
    result = outcome.get_result()
    driver = getattr(item, 'node_driver', None)
    xfail = hasattr(result, 'wasxfail')
    failure = (result.skipped and xfail) or (result.failed and not xfail)
    is_allure_connected = item.config.getoption('--alluredir')
    not_setup_and_teardown = call.when not in ('teardown', 'setup')

    if failure and is_allure_connected and driver:
        for log_type in ['syslog', 'crashlog']:
            logs = driver.get_log(log_type)
            if len(logs):
                allure.attach(str(logs), name=f'Device {log_type} logs', attachment_type=AttachmentType.TEXT)

        if not_setup_and_teardown:
            screenshot_name = f'screenshot_{item.name}'
            screenshot_binary = driver.get_screenshot_as_png()
            allure.attach(resize_image(screenshot_binary), name=screenshot_name, attachment_type=AttachmentType.JPG)
