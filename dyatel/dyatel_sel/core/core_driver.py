from __future__ import annotations

import time
from typing import Union, List, Any

from PIL import Image
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from dyatel.shared_utils import _scaled_screenshot
from selenium.common.exceptions import WebDriverException as SeleniumWebDriverException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.abstraction.driver_wrapper_abc import DriverWrapperABC
from dyatel.dyatel_sel.sel_utils import ActionChains
from dyatel.exceptions import DriverWrapperException, TimeoutException
from dyatel.utils.internal_utils import WAIT_EL, WAIT_UNIT
from dyatel.utils.logs import Logging


class CoreDriver(Logging, DriverWrapperABC):

    driver: Union[AppiumDriver, SeleniumWebDriver]

    def __init__(self, driver: Union[AppiumDriver, SeleniumWebDriver]):
        """
        Initializing of core driver
        Contain same methods/data for both WebDriver and MobileDriver classes

        :param driver: appium or selenium driver to initialize
        """
        driver.implicitly_wait(0.001)  # reduce selenium wait

    def wait(self, timeout: Union[int, float] = WAIT_UNIT) -> CoreDriver:
        """
        Sleep for some time in seconds

        :param timeout: url for navigation
        :return: self
        """
        time.sleep(timeout)
        return self

    def get(self, url: str, silent: bool = False) -> CoreDriver:
        """
        Navigate to given url

        :param url: url for navigation
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Navigating to url {url}')

        try:
            self.driver.get(url)
        except SeleniumWebDriverException as exc:
            raise DriverWrapperException(f'Can\'t proceed to {url}. Original error: {exc.msg}')

        return self

    def screenshot_image(self, screenshot_base: bytes = None) -> Image:
        """
        Get PIL Image object with scaled screenshot of driver window

        :param screenshot_base: screenshot bytes
        :return: PIL Image object
        """
        screenshot_base = screenshot_base if screenshot_base else self.screenshot_base
        return _scaled_screenshot(screenshot_base, self.get_inner_window_size()['width'])

    @property
    def screenshot_base(self) -> bytes:
        """
        Get screenshot base

        :return: screenshot binary
        """
        return self.driver.get_screenshot_as_png()

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

    def quit(self, silent: bool = False, trace_path: str = 'trace.zip'):
        """
        Quit the driver instance

        :param silent: erase log
        :param trace_path: Playwright only: path for the trace
        :return: None
        """
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

    def execute_script(self, script: str, *args) -> Any:
        """
        Synchronously Executes JavaScript in the current window/frame

        :param script: the JavaScript to execute
        :param args: any applicable arguments for your JavaScript (Element object)
        :return: execution return value
        """
        args = [getattr(arg, 'element', arg) for arg in args]
        return self.driver.execute_script(script, *args)

    def set_page_load_timeout(self, timeout: int = 30) -> CoreDriver:
        """
        Set the amount of time to wait for a page load to complete before throwing an error

        :param timeout: timeout to set
        :return: self
        """
        self.driver.set_page_load_timeout(timeout)
        return self

    def switch_to_alert(self, timeout: Union[int, float] = WAIT_EL) -> Alert:
        """
        Wait for alert and switch to it

        :param timeout: timeout to wait
        :return: alert
        """
        alert = None
        end_time = time.time() + timeout

        while not alert and time.time() < end_time:
            try:
                alert = self.driver.switch_to.alert
            except NoAlertPresentException:
                alert = None

        if not alert:
            raise TimeoutException(f'Alert not found after {timeout} seconds')

        return alert

    def accept_alert(self) -> CoreDriver:
        """
        Wait for alert -> switch to it -> click accept

        :return: self
        """
        self.switch_to_alert().accept()
        self.switch_to_default_content()
        return self

    def dismiss_alert(self) -> CoreDriver:
        """
        Wait for alert -> switch to it -> click dismiss

        :return: self
        """
        self.switch_to_alert().dismiss()
        self.switch_to_default_content()
        return self

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
