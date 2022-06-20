import logging
import time

import pytest
import allure
from allure_commons.types import AttachmentType
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver

from dyatel.utils import set_logging_settings, resize_image, shell_running_command, shell_command
from tests.settings import android_desired_caps, android_device_start_timeout, appium_logs_path


set_logging_settings()


def pytest_addoption(parser):
    parser.addoption('--appium-ip', default='0.0.0.0')
    parser.addoption('--appium-port', default='1000')


def is_not_ready_state():
    """ Return True if mobile device is not ready for manipulating """
    return shell_command(f'adb shell getprop sys.boot_completed', capture_output=True).output != '1'


@pytest.fixture(scope='session')
def appium(request):
    """ Programmatically start and stop appium. """
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    service = AppiumService()

    logging.info('Starting appium server')
    service.start(
        args=[
            '-a', appium_ip,
            '-p', appium_port,
            '-g', appium_logs_path,
        ],
        timeout_ms=5000
    )
    assert service.is_running, 'Appium service isn\'t running'
    yield service
    logging.info('Stop Appium server')
    service.stop()
    assert not service.is_running, 'Appium service isn\'t stopped'


@pytest.fixture(scope='session')
def emulator():
    """ Programmatically start and stop emulator. """
    device_name = android_desired_caps['deviceName']
    logging.info(f'Starting emulator {device_name}')
    process = shell_running_command(f'emulator -avd {device_name}')
    logging.info(f'Wait until emulator {device_name} booted:')
    shell_command(f'adb wait-for-device', capture_output=True)
    logging.info(f'1.Emulator {device_name} started')

    start_time = time.time()
    while is_not_ready_state() and android_device_start_timeout > int(time.time() - start_time):
        time.sleep(0.5)

    logging.info(f'2.Emulator {device_name} ready')
    yield process
    serial_number = shell_command('adb get-serialno', capture_output=True).output

    if serial_number:
        logging.info(f'Shutdown emulator "{serial_number}"')
        assert shell_command(f'adb -s {serial_number} emu kill', check=True).is_success

    if process.pid:
        logging.info(f'Kill emulator process by pid "{process.pid}"')
        assert shell_command(f'kill -9 {process.pid}', check=True).is_success


@pytest.fixture
def mobile_driver(request, appium, emulator):
    """ Starting android driver """
    appium_ip = request.config.getoption('--appium-ip')
    appium_port = request.config.getoption('--appium-port')
    command_exc = f'http://{appium_ip}:{appium_port}/wd/hub'
    all_pytest_markers = [marker.name for marker in request.node.own_markers]

    logging.info('Installing & launching android app')
    android_desired_caps.update({'app': 'https://testingbot.com/appium/sample.apk'})
    appium_driver = AppiumDriver(command_executor=command_exc, desired_capabilities=android_desired_caps)
    mobile_driver = MobileDriver(driver=appium_driver)
    logging.info('Android app ready')

    request.node.node_driver = mobile_driver
    yield mobile_driver
    if 'no_teardown' not in all_pytest_markers:
        mobile_driver.terminate_app(mobile_driver.desired_capabilities['appPackage'])  # TODO: fxi issues


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

    if failure and is_allure_connected:

        with open(appium_logs_path, 'r+') as appium_logs_file:
            appium_logs = appium_logs_file.read()
            allure.attach(str(appium_logs), name='Appium logs', attachment_type=AttachmentType.TEXT)
            appium_logs_file.seek(0)
            appium_logs_file.truncate()

        if driver:
            device_logs = driver.get_log('logcat')
            if device_logs:
                device_logs = list(map(lambda log: log['message'], device_logs))  # TODO: find workaround
                allure.attach(str(device_logs), name='Device logs', attachment_type=AttachmentType.TEXT)

            if not_setup_and_teardown:
                screenshot_name = f'screenshot_{item.name}'
                screenshot_binary = driver.get_screenshot_as_png()
                allure.attach(resize_image(screenshot_binary), name=screenshot_name, attachment_type=AttachmentType.JPG)
