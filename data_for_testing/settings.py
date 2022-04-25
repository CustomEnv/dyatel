import os

appium_logs_path = '.tox/.tmp/logs/android_appium.txt'
android_device_start_timeout = 60
android_desired_caps = {
    'avd': 'Pixel3',
    'deviceName': 'Pixel3',
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

ios_desired_caps = {
    'deviceName': 'iPhone 13',
    'platformName': 'iOS',
    'platformVersion': '15.2',
    'automationName': 'XCUITest',
    'udid': 'A2A7D60B-921F-4EDB-8883-203249E9A6DB',
    'app': f'{os.getcwd()}/data_for_testing/apps/sample_app_ios.zip',
    'bundleId': 'io.appium.IosAppSeleniumMaster',
    'newCommandTimeout': 9000,
    'wdaLaunchTimeout': 120000,
}
