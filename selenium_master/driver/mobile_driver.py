from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.webdriver import WebDriver as AppiumDriver

from selenium_master.driver.core_driver import CoreDriver


class MobileDriver(CoreDriver):

    def __init__(self, driver):
        self.mobile_driver: AppiumDriver = driver
        self.capabilities = self.mobile_driver.capabilities

        self.is_ios = self.capabilities.get('platformName') == 'iOS'
        self.is_android = self.capabilities.get('platformName') == 'Android'
        self.is_web = self.capabilities.get('browserName')
        self.is_app = self.capabilities.get('app')

        CoreDriver.driver = self.mobile_driver
        CoreDriver.is_ios = self.is_ios
        CoreDriver.is_android = self.is_android
        CoreDriver.mobile = True

        if self.is_app:
            if self.is_ios:
                self.bundle_id = self.capabilities['bundleId']
            elif self.is_android:
                self.bundle_id = self.capabilities['appPackage']
            else:
                raise Exception('Make sure that correct "platformName" capability specified')

        super(MobileDriver, self).__init__(driver=self.mobile_driver)

    def is_app_installed(self):
        return self.mobile_driver.query_app_state(self.bundle_id) == ApplicationState.RUNNING_IN_FOREGROUND

    def is_app_deleted(self):
        if self.is_ios:  # query_app_state return value equal 1(NOT_RUNNING), that not accurate
            return not self.is_app_installed()

        return self.mobile_driver.query_app_state(self.bundle_id) == ApplicationState.NOT_INSTALLED

    def is_app_closed(self):
        return self.mobile_driver.query_app_state(self.bundle_id) == ApplicationState.NOT_RUNNING

    def is_app_in_foreground(self):
        return self.mobile_driver.query_app_state(self.bundle_id) == ApplicationState.RUNNING_IN_FOREGROUND

    def is_app_in_background(self):
        background_state = ApplicationState.RUNNING_IN_BACKGROUND

        if self.is_ios:  # iOS simulator are suspended the background app
            background_state = ApplicationState.RUNNING_IN_BACKGROUND_SUSPENDED

        return self.mobile_driver.query_app_state(self.bundle_id) == background_state
