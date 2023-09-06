from __future__ import annotations

from abc import ABC
from typing import List, Union, Any

from selenium.webdriver.common.alert import Alert

from dyatel.utils.internal_utils import WAIT_EL


class DriverWrapperABC(ABC):
    session = None
    label = None
    original_tab = None

    driver = None
    browser_name = None

    is_desktop = False
    is_selenium = False
    is_playwright = False

    is_mobile = False
    is_ios = False
    is_android = False
    is_simulator = False
    is_real_device = False

    def quit(self, silent: bool = False):
        """
        Quit the driver instance

        :return: None
        """
        raise NotImplementedError()

    def get_inner_window_size(self) -> dict:
        """
        Get inner size of driver window

        :return: {'height': value, 'width': value}
        """
        raise NotImplementedError()

    def get(self, url: str, silent: bool = False) -> DriverWrapperABC:
        """
        Navigate to given url

        :param url: url for navigation
        :param silent: erase log
        :return: self
        """
        raise NotImplementedError()

    def is_driver_opened(self) -> bool:
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        raise NotImplementedError()

    def is_driver_closed(self) -> bool:
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        raise NotImplementedError()

    @property
    def current_url(self) -> str:
        """
        Get current page url

        :return: url
        """
        raise NotImplementedError()

    def refresh(self) -> DriverWrapperABC:
        """
        Reload current page

        :return: self
        """
        raise NotImplementedError()

    def go_forward(self) -> DriverWrapperABC:
        """
         Go forward by driver

         :return: self
         """
        raise NotImplementedError()

    def go_back(self) -> DriverWrapperABC:
        """
        Go back by driver

        :return: self
        """
        raise NotImplementedError()

    def set_cookie(self, cookies: List[dict]) -> DriverWrapperABC:
        """
        Adds a list of cookie dictionaries to current session

        domain: should be ".google.com" for url "https://google.com/some/url/"

        :param cookies: cookies dictionaries list
        :return: self
        """
        raise NotImplementedError()

    def clear_cookies(self) -> DriverWrapperABC:
        """
        Delete all cookies in the scope of the session

        :return: self
        """
        raise NotImplementedError()

    def delete_cookie(self, name: str) -> DriverWrapperABC:
        """
        Appium/Selenium only: Delete cookie by name

        Playwright does not supported specific cookie removal:
          https://github.com/microsoft/playwright/issues/10143
        todo: possible workaround for playwright:
          https://stackoverflow.com/questions/2144386/how-to-delete-a-cookie

        :return: self
        """
        raise NotImplementedError()

    def get_cookies(self) -> List[dict]:
        """
        Get a list of cookie dictionaries, corresponding to cookies visible in the current session

        :return: cookies dictionaries list
        """
        raise NotImplementedError()

    def switch_to_frame(self, frame: Any) -> DriverWrapperABC:
        """
        Appium/Selenium only: Switch to frame

        :param frame: frame Element
        :return: self
        """
        raise NotImplementedError()

    def switch_to_parent_frame(self) -> DriverWrapperABC:
        """
        Appium/Selenium only: Switch to parent frame from child frame

        :return: self
        """
        raise NotImplementedError()

    def switch_to_default_content(self) -> DriverWrapperABC:
        """
        Appium/Selenium only: Switch to default content from frame

        :return: self
        """
        raise NotImplementedError()

    def execute_script(self, script: str, *args) -> Union[None, str]:
        """
        Synchronously Executes JavaScript in the current window/frame.
        Completable with selenium `execute_script` method

        :param script: the JavaScript to execute
        :param args: any applicable arguments for your JavaScript
        :return: execution return value
        """
        raise NotImplementedError()

    def set_page_load_timeout(self, timeout: int = 30) -> DriverWrapperABC:
        """
        Set the amount of time to wait for a page load to complete before throwing an error

        :param timeout: timeout to set
        :return: self
        """
        raise NotImplementedError()

    def set_window_size(self, width: int, height: int) -> DriverWrapperABC:
        """
        Sets the width and height of the current window

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :return: self
        """
        raise NotImplementedError()

    def get_screenshot(self) -> bytes:
        """
        Gets the screenshot of the current window as a binary data.

        :return: screenshot binary
        """
        raise NotImplementedError()

    def get_all_tabs(self) -> List[DriverWrapperABC]:
        """
        Selenium/Playwright only: Get all opened tabs

        :return: list of tabs
        """
        raise NotImplementedError()

    def create_new_tab(self) -> DriverWrapperABC:
        """
        Selenium/Playwright only: Create new tab and switch into it

        :return: self
        """
        raise NotImplementedError()

    def switch_to_original_tab(self) -> DriverWrapperABC:
        """
        Selenium/Playwright only: Switch to original tab

        :return: self
        """
        raise NotImplementedError()

    def switch_to_tab(self, tab: int = -1) -> DriverWrapperABC:
        """
        Selenium/Playwright only: Switch to specific tab

        :param tab: tab index. Start from 1. Default: latest tab
        :return: self
        """
        raise NotImplementedError()

    def close_unused_tabs(self) -> DriverWrapperABC:
        """
        Selenium/Playwright only: Close all tabs except original

        :return: self
        """
        raise NotImplementedError()

    def click_by_coordinates(self, x: int, y: int, silent: bool = False) -> DriverWrapperABC:
        """
        Click by given coordinates

        :param x: click by given x-axis
        :param y: click by given y-axis
        :param silent: erase log message
        :return: self
        """
        raise NotImplementedError()

    def is_app_installed(self) -> bool:
        """
        Appium only: Is app running checking

        :return: True if the app running
        """
        raise NotImplementedError()

    def is_app_deleted(self) -> bool:
        """
        Appium only: Is app deleted checking

        :return: True if the app deleted
        """
        raise NotImplementedError()

    def is_app_closed(self) -> bool:
        """
        Appium only: Is app closed checking

        :return: True if the app closed
        """
        raise NotImplementedError()

    def is_app_in_foreground(self) -> bool:
        """
        Appium only: Is app in foreground checking

        :return: True if the app in foreground
        """
        raise NotImplementedError()

    def is_app_in_background(self) -> bool:
        """
        Appium only: Is app in background checking

        :return: True if the app in background
        """
        raise NotImplementedError()

    def terminate_app(self, bundle_id) -> bool:
        """
        Appium only: Terminates the application if it is running

        :param bundle_id: the application id to be terminates
        :return: True if the app has been successfully terminated
        """
        raise NotImplementedError()

    def switch_to_native(self) -> DriverWrapperABC:
        """
        Appium only: Switch to native app context

        :return: self
        """
        raise NotImplementedError()

    def switch_to_web(self) -> DriverWrapperABC:
        """
        Appium only: Switch to web app context

        :return: self
        """
        raise NotImplementedError()

    def get_web_view_context(self) -> Union[None, str]:
        """
        Appium only: Get WEBVIEW context name

        :return: None or WEBVIEW context name
        """
        raise NotImplementedError()

    def get_current_context(self) -> str:
        """
        Appium only: Get current context name

        :return: current context name
        """
        raise NotImplementedError()

    def is_native_context(self) -> bool:
        """
        Appium only: Check is current context is native or not

        :return: bool
        """
        raise NotImplementedError()

    def is_web_context(self) -> bool:
        """
        Appium only: Check is current context is web or not

        :return: bool
        """
        raise NotImplementedError()

    def get_all_contexts(self) -> List[str]:
        """
        Appium only: Get the contexts within the current session

        :return: list of available contexts
        """
        raise NotImplementedError()

    def hide_keyboard(self, **kwargs) -> DriverWrapperABC:
        """
        Appium only: Hide keyboard for real device

        :param kwargs: kwargs from Keyboard.hide_keyboard
        :return: MobileDriver
        """
        raise NotImplementedError()

    def get_top_bar_height(self) -> int:
        """
        iOS only: Get top bar height

        :return: self
        """
        raise NotImplementedError()

    def get_bottom_bar_height(self, force: bool = False) -> int:
        """
        iOS only: Get bottom bar height

        :param force: get the new value forcibly
        :return: self
        """
        raise NotImplementedError()

    def switch_to_alert(self, timeout: Union[int, float] = WAIT_EL) -> Alert:
        """
        Appium/Selenium only: Wait for alert and switch to it

        :param timeout: timeout to wait
        :return: alert
        """
        raise NotImplementedError()

    def accept_alert(self) -> DriverWrapperABC:
        """
        Appium/Selenium only: Wait for alert -> switch to it -> click accept

        :return: self
        """
        raise NotImplementedError()

    def dismiss_alert(self) -> DriverWrapperABC:
        """
        Appium/Selenium only: Wait for alert -> switch to it -> click dismiss

        :return: self
        """
        raise NotImplementedError()


