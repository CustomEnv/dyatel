from __future__ import annotations

from typing import List, Union

from playwright.sync_api import Locator, Page
from playwright.sync_api import Browser

from dyatel.abstraction.driver_wrapper_abc import DriverWrapperABC
from dyatel.utils.internal_utils import get_timeout_in_ms
from dyatel.utils.logs import Logging


class PlayDriver(Logging, DriverWrapperABC):

    def __init__(self, driver: Browser):
        """
        Initializing of desktop web driver with playwright

        :param driver: playwright driver to initialize
        """
        self.instance = driver
        self.context = driver.new_context()
        self.driver = self.context.new_page()
        self.original_tab = self.driver
        self.browser_name = self.instance.browser_type.name

    def get(self, url: str, silent: bool = False) -> PlayDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Navigating to url {url}')

        self.driver.goto(url)
        return self

    def is_driver_opened(self) -> bool:
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        return self.instance.is_connected()

    def is_driver_closed(self) -> bool:
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        return not self.instance.is_connected()

    @property
    def current_url(self) -> str:
        """
        Get current page url

        :return: url
        """
        return self.driver.url

    def refresh(self) -> PlayDriver:
        """
        Reload current page

        :return: self
        """
        self.log('Reload current page')
        self.driver.reload()
        return self

    def go_forward(self) -> PlayDriver:
        """
        Go forward by driver

        :return: self
        """
        self.log('Going forward')
        self.driver.go_forward()
        return self

    def go_back(self) -> PlayDriver:
        """
        Go back by driver

        :return: self
        """
        self.log('Going back')
        self.driver.go_back()
        return self

    def quit(self) -> None:
        """
        Quit the driver instance

        :return: None
        """
        self.driver.close()

    def set_cookie(self, cookies: List[dict]) -> PlayDriver:
        """
        Adds a list of cookie dictionaries to current session

        domain: should be ".google.com" for url "https://google.com/some/url/"

        :param cookies: cookies dictionaries list
        :return: self
        """
        for cookie in cookies:

            if 'path' not in cookie:
                cookie.update({'path': '/'})

            if 'domain' not in cookie:
                cookie.update({'domain': f'.{self.current_url.split("://")[1].split("/")[0]}'})

        self.context.add_cookies(cookies)
        return self

    def clear_cookies(self) -> PlayDriver:
        """
        Delete all cookies in the scope of the session

        :return: self
        """
        self.context.clear_cookies()
        return self

    def get_cookies(self) -> List[dict]:
        """
        Get a list of cookie dictionaries, corresponding to cookies visible in the current session

        :return: cookies dictionaries list
        """
        return self.context.cookies()

    def execute_script(self, script: str, *args) -> Union[None, str]:
        """
        Synchronously Executes JavaScript in the current window/frame.
        Completable with selenium `execute_script` method

        :param script: the JavaScript to execute
        :param args: any applicable arguments for your JavaScript
        :return: execution return value
        """
        script = script.replace('return ', '')

        script_args = list(args)
        if 'arguments[0]' in script:
            script_args = [*args]
            script = f'arguments => {{{script}}}'

        for index, arg in enumerate(args):
            if isinstance(arg, Locator):
                script_args[index] = arg.element_handle()

        return self.driver.evaluate(script, script_args)

    def set_page_load_timeout(self, timeout: int = 30) -> PlayDriver:
        """
        Set the amount of time to wait for a page load to complete before throwing an error

        :param timeout: timeout to set in seconds
        :return: self
        """
        self.driver.set_default_navigation_timeout(get_timeout_in_ms(timeout))
        return self

    def set_window_size(self, width: int, height: int) -> PlayDriver:
        """
        Sets the width and height of the current window

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :return: self
        """
        self.driver.set_viewport_size({'width': width, 'height': height})
        return self

    def get_screenshot(self) -> bytes:
        """
        Gets the screenshot of the current window as a binary data.

        :return: screenshot binary
        """
        return self.driver.screenshot()

    def get_all_tabs(self) -> List[Page]:
        """
        Get all opened tabs

        :return: list of tabs
        """
        return self.context.pages

    def create_new_tab(self) -> PlayDriver:
        """
        Create new tab and switch into it

        :return: self
        """
        with self.context.expect_page() as new_page:
            self.execute_script("window.open(arguments[0], '_blank').focus();", self.current_url)

        self.driver = new_page.value
        return self

    def switch_to_original_tab(self) -> PlayDriver:
        """
        Switch to original tab

        :return: self
        """
        self.driver = self.original_tab
        self.driver.bring_to_front()
        return self

    def switch_to_tab(self, tab: int = -1) -> PlayDriver:
        """
        Switch to specific tab

        :param tab: tab index. Start from 1. Default: latest tab
        :return: self
        """
        if tab == -1:
            tab = self.get_all_tabs()[tab]
        else:
            tab = self.get_all_tabs()[tab - 1]

        self.driver = tab
        self.driver.bring_to_front()
        return self

    def close_unused_tabs(self) -> PlayDriver:
        """
        Close all tabs except original

        :return: self
        """
        tabs = self.get_all_tabs()
        tabs.remove(self.original_tab)

        for tab in tabs:
            tab.close()

        return self.switch_to_original_tab()

    def click_by_coordinates(self, x: int, y: int, silent: bool = False) -> PlayDriver:
        """
        Click by given coordinates

        :param x: click by given x-axis
        :param y: click by given y-axis
        :param silent: erase log message
        :return: self
        """
        if not silent:
            self.log(f'Click by given coordinates (x: {x}, y: {y})')

        self.driver.mouse.click(x=x, y=y)
        return self
