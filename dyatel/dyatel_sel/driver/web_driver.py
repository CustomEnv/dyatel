from typing import List

from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver


class WebDriver(CoreDriver):

    def __init__(self, driver: SeleniumWebDriver, *args, **kwargs):  # noqa
        """
        Initializing of desktop web driver with selenium

        :param driver: selenium driver to initialize
        """
        self.is_desktop = True
        self.original_tab = driver.current_window_handle
        self.browser_name = driver.caps.get('browserName', None)

        CoreDriver.__init__(self, driver=driver)

    def set_window_size(self, width: int, height: int) -> CoreDriver:
        """
        Sets the width and height of the current window

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :return: self
        """
        self.driver.set_window_size(width, height)
        return self

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
