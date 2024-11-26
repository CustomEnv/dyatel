from __future__ import annotations

from typing import Union, List, Optional

from appium.webdriver.applicationstate import ApplicationState
from appium.webdriver.webdriver import WebDriver as AppiumDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.mixins.native_context import NativeContext, NativeSafari


class MobileDriver(CoreDriver):

    bundle_id: Optional[str]

    def __init__(self, driver: AppiumDriver, *args, **kwargs):  # noqa
        """
        Initializing of mobile driver with appium

        :param driver: appium driver to initialize
        """
        self.caps = driver.capabilities
        self.browser_name = self.caps.get('browserName', None)
        self.is_web = bool(self.browser_name) or False
        self.is_app = self.caps.get('app', False)

        _set_static(self)

        self.native_context_name = 'NATIVE_APP'
        self.web_context_name = self.get_web_view_context() if self.is_ios else 'CHROMIUM'
        self.__is_native_context = None
        self.__is_web_context = None

        self._top_bar_height = None
        self._bottom_bar_height = None

        self.original_tab = None
        self.page_box = None

        self.native_safari = NativeSafari(self)

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
        self.driver.switch_to.context(self.native_context_name)
        self.__is_native_context = True
        self.__is_web_context = False
        return self

    def switch_to_web(self) -> MobileDriver:
        """
        Switch to web app context

        :return: self
        """
        self.driver.switch_to.context(self.web_context_name)
        self.__is_native_context = False
        self.__is_web_context = True
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

    @property
    def is_native_context(self) -> bool:
        """
        Check is current context is native or not

        :return: bool
        """
        if self.__is_native_context is None:
            self.__is_native_context = self.get_current_context() == self.native_context_name

        return self.__is_native_context

    @property
    def is_web_context(self) -> bool:
        """
        Check is current context is web or not

        :return: bool
        """
        if self.__is_web_context is None:
            self.__is_web_context = self.get_current_context() == self.web_context_name

        return self.__is_web_context

    @property
    def top_bar_height(self) -> int:
        """
        iOS only: Get top bar height

        :return: self
        """
        if self._top_bar_height is None:
            with NativeContext(self):
                self._top_bar_height = self.native_safari.top_bar.size.height

        return self._top_bar_height

    @property
    def bottom_bar_height(self) -> int:
        """
        iOS only: Get bottom bar height

        :return: self
        """
        if self.is_tablet:
            return 0

        if self._bottom_bar_height is None:
            with NativeContext(self):
                self._bottom_bar_height = self.native_safari.get_bottom_bar_height()

        return self._bottom_bar_height

    def get_all_contexts(self) -> List[str]:
        """
        Get the contexts within the current session

        :return: list of available contexts
        """
        return self.driver.contexts

    def screenshot_image(self, screenshot_base: bytes = None):
        """
        Get driver width scaled screenshot binary of element without saving
        iOS: remove native controls from image manually

        :param screenshot_base: screenshot bytes
        :return: screenshot binary
        """
        image = CoreDriver.screenshot_image(self, screenshot_base)

        if self.is_ios and not screenshot_base:
            if not self.page_box:
                width, height = image.size
                self.page_box = 0, self.top_bar_height, width, height - self.bottom_bar_height

            image = image.crop(self.page_box)

        return image

    def hide_keyboard(self, **kwargs) -> MobileDriver:
        """
        Hide keyboard for real device

        :param kwargs: kwargs from Keyboard.hide_keyboard
        :return: MobileDriver
        """
        if self.is_real_device:
            self.driver.hide_keyboard(**kwargs)

        elif self.is_ios and self.is_simulator:
            with NativeContext(self):
                if self.native_safari.keyboard_done_button.is_displayed():
                    self.native_safari.keyboard_done_button.click()

        return self

    def click_by_coordinates(self, x: int, y: int, silent: bool = False) -> MobileDriver:
        """
        Click by given coordinates

        :param x: tap by given x-axis
        :param y: tap by given y-axis
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Tap by given coordinates (x: {x}, y: {y})')

        if self.is_ios:
            self.driver.tap(positions=[(x, y)])
        elif self.is_android:
            CoreDriver.click_by_coordinates(self, x=x, y=y, silent=True)

        return self


def _set_static(obj) -> None:
    """
    Set static attributes for Appium driver wrapper

    :return: None
    """
    obj.is_tablet = obj.caps.get('is_tablet', False)
    obj.is_mobile = not obj.is_tablet

    obj.is_ios = obj.caps.get('platformName').lower() == 'ios'
    obj.is_ios_tablet = obj.is_ios and obj.is_tablet
    obj.is_ios_mobile = obj.is_ios and obj.is_mobile

    obj.is_android = obj.caps.get('platformName').lower() == 'android'
    obj.is_android_tablet = obj.is_android and obj.is_tablet
    obj.is_android_mobile = obj.is_android and obj.is_mobile

    obj.is_simulator = obj.caps.get('useSimulator', False)
    obj.is_real_device = not obj.is_simulator

    if obj.is_app:
        if obj.is_ios:
            obj.bundle_id = obj.caps.get('bundleId', 'undefined: bundleId')
        elif obj.is_android:
            obj.bundle_id = obj.caps.get('appPackage', 'undefined: appPackage')
        else:
            raise Exception('Make sure that correct "platformName" capability specified')
