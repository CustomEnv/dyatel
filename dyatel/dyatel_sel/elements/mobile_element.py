from __future__ import annotations

from typing import Union, List, BinaryIO, Any

from appium.webdriver.common.touch_action import TouchAction

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.sel_utils import get_legacy_selector, get_locator_type
from dyatel.mixins.internal_utils import calculate_coordinate_to_click, WAIT_EL
from dyatel.js_scripts import get_element_position_on_screen_js, get_element_size_js, click_js, is_displayed_js


class MobileElement(CoreElement):

    def __init__(self, locator: str, locator_type: str = '', name: str = '',
                 parent: Union[MobileElement, Any] = None, wait: bool = False):
        """
        Initializing of mobile element with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be MobileElement, MobilePage, Group objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self.is_safari_driver = CoreDriver.is_safari_driver
        self.is_ios = CoreDriver.is_ios
        self.is_android = CoreDriver.is_android

        self.locator_type = locator_type if locator_type else get_locator_type(locator)
        self.locator, self.locator_type = get_legacy_selector(locator, self.locator_type)

        super().__init__(locator=self.locator, locator_type=self.locator_type, name=name, parent=parent, wait=wait)

    @property
    def all_elements(self) -> List[Any]:
        """
        Get all wrapped elements with appium bases

        :return: list of wrapped objects
        """
        appium_elements = self._find_elements(self._get_base())
        return self._get_all_elements(appium_elements, MobileElement)

    def wait_element(self, timeout: int = WAIT_EL, silent: bool = False) -> MobileElement:
        """
        Wait for current element available in page
        SafariDriver: Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if self.is_safari_driver:
            self.wait_availability(timeout=timeout, silent=True)
        else:
            super().wait_element(timeout=timeout, silent=silent)

        return self

    def click(self) -> MobileElement:
        """
        Click to current element
        SafariDriver: Click to current element by JS

        :return: self
        """
        if self.is_safari_driver:
            self.wait_element(silent=True).wait_clickable(silent=True)
            self.driver.execute_script(click_js, self.element)
        else:
            super().click()

        return self

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of element
        SafariDriver: Check visibility by JS

        :param: silent: erase log
        :return: True if element visible
        """
        if self.is_safari_driver:
            if not silent:
                self.log(f'Check displaying of "{self.name}"')

            try:
                return self.driver_wrapper.execute_script(is_displayed_js, self._get_element(wait=False))
            except:
                return False
        else:
            return super().is_displayed(silent=silent)

    def hover(self) -> MobileElement:
        """
        Hover over current element

        :return: self
        """
        self.log(f'Tap to "{self.name}"')
        self.wait_element(silent=True)

        if self.is_ios:
            x, y = calculate_coordinate_to_click(self, 0, 0)
            TouchAction(self.driver).tap(x=x, y=y).perform()
        else:
            self._action_chains.click(on_element=self.element).perform()

        return self

    def hover_outside(self, x: int = 0, y: int = -5) -> MobileElement:
        """
        Hover outside from current element

        :return: self
        """
        return self.click_outside(x, y)

    def click_outside(self, x: int = 0, y: int = -5) -> MobileElement:
        """
        Click outside of element. By default, 5px above  of element

        :param x: x offset
        :param y: y offset
        :return: self
        """
        self.log(f'Tap outside from "{self.name}"')
        self.wait_element(silent=True)

        x, y = calculate_coordinate_to_click(self, x, y)

        if self.is_ios:
            TouchAction(self.driver).tap(x=x, y=y).perform()
        else:
            self._action_chains.move_to_location(x, y).click().perform()
        return self

    def get_screenshot(self, filename: str, legacy: bool = True) -> BinaryIO:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :param legacy: iOS only - crop element for page screenshot manually
        :return: image binary
        """
        if self.driver_wrapper.is_ios and legacy:
            element_box = self._element_box()
            window_width, window_height = self.driver.get_window_size().values()
            img_binary = self.driver_wrapper.get_screenshot()
            image_binary = self._scaled_screenshot(img_binary, window_width)

            if any(element_box) < 0 or window_height > self.element.size['height']:
                image_binary = image_binary.crop(element_box)

            image_binary.save(filename)
        else:
            image_binary = super().get_screenshot(filename)

        return image_binary

    def get_rect(self) -> dict:
        """
        A dictionary with the size and location of the element.

        :return: dict
        """
        element = self.element
        size = self.driver.execute_script(get_element_size_js, element)
        location = self.driver.execute_script(get_element_position_on_screen_js, element)

        return {**size, **location}

    def _element_box(self) -> tuple:
        """
        Get element coordinates on screen for ios safari

        :return: element coordinates on screen (start_x, start_y, end_x, end_y)
        """
        element = self.element
        el_location = self.driver.execute_script(get_element_position_on_screen_js, element)
        start_x, start_y = el_location.values()
        h, w = element.size.values()

        if self.is_safari_driver:
            inner_height = self.driver.execute_script('return window.innerHeight')
            outer_height = self.driver.execute_script('return window.outerHeight')
            bars_size = outer_height - inner_height

            if bars_size > 110:  # There is no way to get top/bottom bars of safari with SafariDriver
                bar_size = bars_size / 4  # top and bottom bar shown
            else:
                bar_size = bars_size / 2  # top bar shown, bottom hidden
        else:
            bar_size = self.driver_wrapper.get_top_bar_height()

        if bar_size:
            start_y += bar_size

        return start_x, start_y, start_x+w, start_y+h
