from __future__ import annotations

from logging import info
from typing import List, Union

from playwright.sync_api import Page as PlaywrightPage, Locator
from playwright.sync_api import Browser

from dyatel.internal_utils import Mixin, get_timeout_in_ms


class PlayDriver(Mixin):
    instance: Browser = None
    driver: PlaywrightPage = None
    driver_wrapper: PlayDriver = None

    mobile = False
    desktop = False
    is_ios = False
    is_android = False

    def __init__(self, driver: Browser):
        """
        Initializing of desktop web driver with playwright

        :param driver: playwright driver to initialize
        """
        self.driver_context = driver.new_context()
        context = self.driver_context.new_page()
        self.driver = context
        PlayDriver.desktop = True

        if not PlayDriver.driver:
            PlayDriver.instance = driver
            PlayDriver.driver = context
            PlayDriver.driver_wrapper = self

    def get(self, url) -> PlayDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :return: self
        """
        info(f'Navigating to url {url}')
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
        info('Reload current page')
        self.driver.reload()
        return self

    def go_forward(self) -> PlayDriver:
        """
        Go forward by driver

        :return: self
        """
        info('Going forward')
        self.driver.go_forward()
        return self

    def go_back(self) -> PlayDriver:
        """
        Go back by driver

        :return: self
        """
        info('Going back')
        self.driver.go_back()
        return self

    def quit(self, silent=True) -> PlayDriver:
        """
        Quit the driver instance

        :param: silent:
        :return: self
        """
        if silent:
            info('Quit driver instance')

        self.driver.close()
        return self

    def set_cookie(self, cookies: List[dict]) -> PlayDriver:
        """
        Adds a list of cookie dictionaries to current session

        :param cookies: cookies dictionaries list
        :return: self
        """
        self.driver_context.add_cookies(cookies)
        return self

    def clear_cookies(self) -> PlayDriver:
        """
        Delete all cookies in the scope of the session

        :return: self
        """
        self.driver_context.clear_cookies()
        return self

    def get_cookies(self) -> List[dict]:
        """
        Get a list of cookie dictionaries, corresponding to cookies visible in the current session

        :return: cookies dictionaries list
        """
        return self.driver_context.cookies()

    def execute_script(self, script, *args) -> Union[None, str]:
        """
        Synchronously Executes JavaScript in the current window/frame.
        Completable with selenium `execute_script` method

        :param script: the JavaScript to execute
        :param args: any applicable arguments for your JavaScript
        :return: execution return value
        """
        script = script.replace('return ', '')

        script_args = args
        if 'arguments[0]' in script:
            script_args = [*args]
            script = f'arguments => {script}'

        for index, arg in enumerate(args):
            if isinstance(arg, Locator):
                script_args[index] = arg.element_handle()

        return self.driver.evaluate(script, script_args)

    def set_page_load_timeout(self, timeout=30) -> PlayDriver:
        """
        Set the amount of time to wait for a page load to complete before throwing an error

        :param timeout: timeout to set
        :return: self
        """
        self.driver.set_default_navigation_timeout(get_timeout_in_ms(timeout))
        return self

    def set_window_size(self, width, height) -> PlayDriver:
        """
        Sets the width and height of the current window

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :return: self
        """
        self.driver.set_viewport_size({'width': width, 'height': height})
        return self
