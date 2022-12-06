domain_name = 'https://envinc.github.io/'
repo_name = 'dyatel-playground'

appium_logs_path = '.tox/.tmp/logs/android_appium.txt'
android_device_start_timeout = 60
android_desired_caps = {
    'avd': 'Pixel5',
    'deviceName': 'Pixel5',
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
    'deviceName': 'iPhone 13',
    'platformName': 'iOS',
    'platformVersion': '15.4',
    'automationName': 'XCUITest',
    'udid': 'FD714443-9CA8-4B85-A767-7CD9A3168E39',
    # Update following capabilities before driver init
    # 'app': f'{os.getcwd()}/data_for_testing/apps/sample_app_ios.zip',
    # 'browserName': 'Safari',
    # 'bundleId': 'io.appium.IosAppSeleniumMaster',
    'newCommandTimeout': 9000,
    'wdaLaunchTimeout': 120000,
}
