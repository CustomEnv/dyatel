from __future__ import annotations

import time
from typing import Union, List

from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.common.by import By

from dyatel.dyatel_sel.core.core_driver import CoreDriver


class MobileDriver(CoreDriver):

    def __init__(self, driver: AppiumDriver):
        """
        Initializing of mobile driver with appium

        :param driver: appium driver to initialize
        """
        self.capabilities = driver.capabilities

        self.is_web = self.capabilities.get('browserName', False)
        self.is_app = self.capabilities.get('app', False)
        self.is_android = self.capabilities.get('platformName').lower() == 'android'

        self.is_ios = self.capabilities.get('platformName').lower() == 'ios'
        self.is_safari_driver = self.capabilities.get('automationName').lower() == 'safari'
        self.is_xcui_driver = self.capabilities.get('automationName').lower() == 'xcuitest'

        CoreDriver.mobile = True
        CoreDriver.is_ios = self.is_ios
        CoreDriver.is_android = self.is_android
        CoreDriver.is_safari_driver = self.is_safari_driver
        CoreDriver.is_xcui_driver = self.is_xcui_driver

        self.native_context = 'NATIVE_APP'
        self.web_context = self.get_web_view_context() if self.is_xcui_driver else 'CHROMIUM'

        self.top_bar_height = None
        self.bottom_bar_height = None

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

    def switch_to_native(self) -> MobileDriver:
        """
        Switch to native app context

        :return: self
        """
        self.driver.switch_to.context(self.native_context)
        return self

    def switch_to_web(self) -> MobileDriver:
        """
        Switch to web app context

        :return: self
        """
        self.driver.switch_to.context(self.web_context)
        return self

    def get_web_view_context(self) -> Union[None, str]:
        """
        Get WEBVIEW context name

        :return: None or WEBVIEW context name
        """
        for context in self.get_all_contexts():
            if 'WEBVIEW' in context:
                return context

    def get_current_context(self) -> str:
        """
        Get current context name

        :return: current context name
        """
        return self.driver.context

    def get_all_contexts(self) -> List[str]:
        """
        Get the contexts within the current session

        :return: list of available contexts
        """
        return self.driver.contexts

    def get_top_bar_height(self) -> int:
        """
        iOS only: Get top bar height

        :return: self
        """
        if not self.top_bar_height:
            self.switch_to_native()

            top_bar = self.driver.find_element(
                By.XPATH,
                '//*[contains(@name, "SafariWindow")]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther'
            )
            top_bar_height = top_bar.size['height']

            self.switch_to_web()
            return top_bar_height
        else:
            return self.top_bar_height

    def get_bottom_bar_height(self, force: bool = False) -> int:
        """
        iOS only: Get bottom bar height

        :param force: get the new value forcly
        :return: self
        """
        if force or not self.top_bar_height:
            self.switch_to_native()

            bottom_bar = self.driver.find_element(
                By.XPATH,
                '//*[@name="CapsuleViewController"]/XCUIElementTypeOther[1]'
            )
            bottom_bar_height = bottom_bar.size['height']

            self.switch_to_web()
            return bottom_bar_height
        else:
            return self.top_bar_height
