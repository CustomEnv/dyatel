from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.webdriver import WebDriver as AppiumDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver


class MobileDriver(CoreDriver):

    def __init__(self, driver: AppiumDriver):
        """
        Initializing of mobile driver with appium

        :param driver: appium driver to initialize
        """
        self.capabilities = driver.capabilities

        self.is_ios = self.capabilities.get('platformName') == 'iOS'
        self.is_android = self.capabilities.get('platformName') == 'Android'
        self.is_web = self.capabilities.get('browserName', False)
        self.is_app = self.capabilities.get('app', False)

        CoreDriver.is_ios = self.is_ios
        CoreDriver.is_android = self.is_android
        CoreDriver.mobile = True
        CoreDriver.desktop = False

        if self.is_app:
            if self.is_ios:
                self.bundle_id = self.capabilities['bundleId']
            elif self.is_android:
                self.bundle_id = self.capabilities['appPackage']
            else:
                raise Exception('Make sure that correct "platformName" capability specified')

        CoreDriver.__init__(self, driver=driver)

    def is_app_installed(self) -> bool:
        """
        Is app running checking

        :return: True if the app running
        """
        return self.driver.query_app_state(self.bundle_id) == ApplicationState.RUNNING_IN_FOREGROUND

    def is_app_deleted(self) -> bool:
        """
        Is app deleted checking

        :return: True if the app deleted
        """
        if self.is_ios:  # query_app_state return value equal 1(NOT_RUNNING), that not accurate
            return not self.is_app_installed()

        return self.driver.query_app_state(self.bundle_id) == ApplicationState.NOT_INSTALLED

    def is_app_closed(self) -> bool:
        """
        Is app closed checking

        :return: True if the app closed
        """
        return self.driver.query_app_state(self.bundle_id) == ApplicationState.NOT_RUNNING

    def is_app_in_foreground(self) -> bool:
        """
        Is app in foreground checking

        :return: True if the app in foreground
        """
        return self.driver.query_app_state(self.bundle_id) == ApplicationState.RUNNING_IN_FOREGROUND

    def is_app_in_background(self) -> bool:
        """
        Is app in background checking

        :return: True if the app in background
        """
        background_state = ApplicationState.RUNNING_IN_BACKGROUND

        if self.is_ios:  # iOS simulator are suspended the background app
            background_state = ApplicationState.RUNNING_IN_BACKGROUND_SUSPENDED

        return self.driver.query_app_state(self.bundle_id) == background_state

    def terminate_app(self, bundle_id) -> bool:
        """
        Terminates the application if it is running

        :param bundle_id: the application id to be terminates
        :return: True if the app has been successfully terminated
        """
        return self.driver.terminate_app(bundle_id)
