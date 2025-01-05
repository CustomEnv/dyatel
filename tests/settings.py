import os

domain_name = 'https://customenv.github.io'
repo_name = 'dyatel-playground'

appium_logs_path = '.tox/.tmp/logs/android_appium.txt'
android_device_start_timeout = 60

def get_android_desired_caps():
    env = os.environ
    print('Env variables: ', env)

    return {
        'deviceName': env.get('DEVICE_NAME') or 'emulator-5555',
        'platformName': 'Android',
        'platformVersion': env.get('PLATFORM_VERSION') or '11.0',
        # Update following capabilities before driver init
        # 'app': 'https://testingbot.com/appium/sample.apk',
        # 'browserName': 'Chrome',
        'automationName': 'UiAutomator2',
        'noReset': True,
        'newCommandTimeout': 3000,
        'avdLaunchTimeout': 120000,
        'avdReadyTimeout': 120000,
        'adbExecTimeout': 120000,
    }

ios_desired_caps = {
    'automationName': 'XCUITest',
    'platformName': 'iOS',
    'deviceName': 'iPhone 12 mini',
    'platformVersion': '15.5',
    'browserName': 'Safari',
    'autoWebview': True,
    'useSimulator': True,
    'udid': '8239C85D-88C1-45B8-BD40-BB3AD3115A67',
    'newCommandTimeout': 3000,
    'wdaLaunchTimeout': 120000,
}
