from __future__ import annotations

from typing import Union, List, Any

from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.sel_utils import ActionChains
from dyatel.exceptions import DriverWrapperException
from dyatel.mixins.log_mixin import LogMixin


class CoreDriver(LogMixin):
    all_drivers: Union[List[AppiumDriver], List[SeleniumWebDriver]] = []
    driver: Union[AppiumDriver, SeleniumWebDriver] = None
    driver_wrapper = None

    def __init__(self, driver: Union[AppiumDriver, SeleniumWebDriver]):
        """
        Initializing of core driver
        Contain same methods/data for both WebDriver and MobileDriver classes

        :param driver: appium or selenium driver to initialize
        """
        driver.implicitly_wait(0.001)  # reduce selenium wait
        self.driver = driver
        self.driver_wrapper: Any = self
        self.all_drivers.append(driver)
        self.original_tab = driver.current_window_handle

        if not CoreDriver.driver:
            CoreDriver.driver = driver
            CoreDriver.driver_wrapper = self

    def get(self, url: str) -> CoreDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :return: self
        """
        self.log(f'Navigating to url {url}')

        try:
            self.driver.get(url)
        except WebDriverException:
            raise DriverWrapperException(f'Can\'t proceed to {url}')

        return self

    def is_driver_opened(self) -> bool:
        """
        Check is driver opened or not

        :return: True if driver opened
        """
        return True if self.driver else False

    def is_driver_closed(self) -> bool:
        """
        Check is driver closed or not

        :return: True if driver closed
        """
        return False if self.driver else True

    @property
    def current_url(self) -> str:
        """
        Get current page url

        :return: url
        """
        return self.driver.current_url

    def refresh(self) -> CoreDriver:
        """
        Reload current page

        :return: self
        """
        self.log('Reload current page')
        self.driver.refresh()
        return self

    def go_forward(self) -> CoreDriver:
        """
        Go forward by driver

        :return: self
        """
        self.log('Going forward')
        self.driver.forward()
        return self

    def go_back(self) -> CoreDriver:
        """
        Go back by driver

        :return: self
        """
        self.log('Going back')
        self.driver.back()
        return self

    def quit(self, silent: bool = True) -> None:
        """
        Quit the driver instance

        :param: silent:
        :return: None
        """
        if silent:
            self.log('Quit driver instance')

        self.driver.quit()

    def set_cookie(self, cookies: List[dict]) -> CoreDriver:
        """
        Adds a list of cookie dictionaries to current session

        :param cookies: cookies dictionaries list
        :return: self
        """
        for cookie in cookies:
            cookie.pop('domain', None)

            if 'path' not in cookie:
                cookie.update({'path': '/'})

            self.driver.add_cookie(cookie)

        return self

    def clear_cookies(self) -> CoreDriver:
        """
        Delete all cookies in the scope of the session

        :return: self
        """
        self.driver.delete_all_cookies()
        return self

    def delete_cookie(self, name: str) -> CoreDriver:
        """
        Delete cooke by name

        :return: self
        """
        self.driver.delete_cookie(name)
        return self

    def get_cookies(self) -> List[dict]:
        """
        Get a list of cookie dictionaries, corresponding to cookies visible in the current session

        :return: cookies dictionaries list
        """
        return self.driver.get_cookies()

    def switch_to_frame(self, frame: Any) -> CoreDriver:
        """
        Switch to frame

        :param frame: frame Element
        :return: self
        """
        self.driver.switch_to.frame(frame.element)
        return self

    def switch_to_parent_frame(self) -> CoreDriver:
        """
        Switch to parent frame from child frame

        :return: self
        """
        self.driver.switch_to.parent_frame()
        return self

    def switch_to_default_content(self) -> CoreDriver:
        """
        Switch to default content from frame

        :return: self
        """
        self.driver.switch_to.default_content()
        return self

    def execute_script(self, script: str, *args):
        """
        Synchronously Executes JavaScript in the current window/frame

        :param script: the JavaScript to execute
        :param args: any applicable arguments for your JavaScript
        :return: execution return value
        """
        return self.driver.execute_script(script, *args)

    def set_page_load_timeout(self, timeout: int = 30) -> CoreDriver:
        """
        Set the amount of time to wait for a page load to complete before throwing an error

        :param timeout: timeout to set
        :return: self
        """
        self.driver.set_page_load_timeout(timeout)
        return self

    def set_window_size(self, width: int, height: int) -> CoreDriver:
        """
        Sets the width and height of the current window

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :return: self
        """
        self.driver.set_window_size(width, height)
        return self

    def get_screenshot(self) -> bytes:
        """
        Gets the screenshot of the current window as a binary data.

        :return: screenshot binary
        """
        return self.driver.get_screenshot_as_png()

    def get_all_tabs(self) -> List[str]:
        """
        Get all opened tabs

        :return: list of tabs
        """
        return self.driver.window_handles

    def create_new_tab(self) -> CoreDriver:
        """
        Create new tab and switch into it

        :return: self
        """
        self.driver.switch_to.new_window('tab')
        return self

    def switch_to_original_tab(self) -> CoreDriver:
        """
        Switch to original tab

        :return: self
        """
        self.driver.switch_to.window(self.original_tab)
        return self

    def switch_to_tab(self, tab=-1) -> CoreDriver:
        """
        Switch to specific tab

        :param tab: tab index. Start from 1. Default: latest tab
        :return: self
        """
        if tab == -1:
            tab = self.get_all_tabs()[tab]
        else:
            tab = self.get_all_tabs()[tab - 1]

        self.driver.switch_to.window(tab)
        return self

    def close_unused_tabs(self) -> CoreDriver:
        """
        Close all tabs except original

        :return: self
        """
        tabs = self.get_all_tabs()
        tabs.remove(self.original_tab)

        for tab in tabs:
            self.driver.switch_to.window(tab)
            self.driver.close()

        return self.switch_to_original_tab()

    def click_by_coordinates(self, x: int, y: int, silent: bool = False) -> CoreDriver:
        """
        Click by given coordinates

        :param x: click by given x-axis
        :param y: click by given y-axis
        :param silent: erase log message
        :return: self
        """
        if not silent:
            self.log(f'Click by given coordinates (x: {x}, y: {y})')

        ActionChains(self.driver).move_to_location(x, y).click().perform()
        return self
