domain_name = 'https://envinc.github.io/'
repo_name = 'dyatel-playground'

appium_logs_path = '.tox/.tmp/logs/android_appium.txt'
android_device_start_timeout = 60
android_desired_caps = {
    'avd': 'Pixel4',
    'deviceName': 'Pixel4',
    'platformName': 'Android',
    'platformVersion': '12.0',
    # Update following capabilities before driver init
    # 'app': 'https://testingbot.com/appium/sample.apk',
    # 'browserName': 'Chrome',
    'automationName': 'UiAutomator2',
    'noReset': True,
    'newCommandTimeout': 9000,
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
    'udid': '2B4EA039-5225-43DF-A10D-EDEFD26400A1',
    'newCommandTimeout': 9000,
    'wdaLaunchTimeout': 120000,
}
