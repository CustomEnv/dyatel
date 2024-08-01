from __future__ import annotations

import time
from abc import ABC
from typing import Union

from PIL.Image import Image

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.mixins.objects.location import Location
from dyatel.mixins.objects.locator import Locator, take_locator_type
from dyatel.mixins.objects.size import Size
from dyatel.utils.internal_utils import calculate_coordinate_to_click
from dyatel.utils.selector_synchronizer import get_platform_locator, get_selenium_locator_type, get_appium_selector


class MobileElement(CoreElement, ABC):

    def __init__(self, locator: Union[Locator, str]):
        """
        Initializing of mobile element with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        """
        self.locator = get_platform_locator(self)
        locator_type = take_locator_type(locator) or get_selenium_locator_type(self.locator)
        self.locator, self.locator_type = get_appium_selector(self.locator, locator_type)

    def click_outside(self, x: int = 0, y: int = -5) -> MobileElement:
        """
        Click outside of element. By default, 5px above  of element

        :param x: x offset of element to tap
        :param y: y offset of element to tap
        :return: self
        """
        if self.driver_wrapper.is_web_context:
            if not self.is_fully_visible(silent=True):
                self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, x, y)

        if self.driver_wrapper.is_ios:
            y += self.driver_wrapper.top_bar_height

        self.log(f'Tap outside from "{self.name}" with coordinates (x: {x}, y: {y})')

        self.driver_wrapper.click_by_coordinates(x=x, y=y, silent=True)
        return self

    def click_into_center(self, silent: bool = True) -> MobileElement:
        """
        Click into the center of element

        :param silent: erase log message
        :return: self
        """
        if self.driver_wrapper.is_web_context:
            if not self.is_fully_visible(silent=True):
                self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, 0, 0)

        if self.driver_wrapper.is_ios:
            y += self.driver_wrapper.top_bar_height

        if not silent:
            self.log(f'Tap into the center by coordinates (x: {x}, y: {y}) for "{self.name}"')

        self.driver_wrapper.click_by_coordinates(x, y, silent=True)

        return self

    def hover(self, silent: bool = False) -> MobileElement:
        """
        Hover over current element

        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Hover over "{self.name}"')

        self.click_into_center()
        return self

    def hover_outside(self, x: int = 0, y: int = -5) -> MobileElement:
        """
        Hover outside from current element. By default, 5px above  of element

        :param x: x-offset of element to hover(tap)
        :param y: y-offset of element to hover(tap)
        :return: self
        """
        return self.click_outside(x=x, y=y)

    def click_in_alert(self) -> MobileElement:
        """
        Click on element in alert with switch to native context

        :return: self
        """
        try:
            self.driver_wrapper.switch_to_native()
            time.sleep(1)
            if self.wait_visibility_without_error(timeout=5, silent=True).is_displayed(silent=True):
                self.click()
        finally:
            self.driver_wrapper.switch_to_web()

        return self

    def screenshot_image(self, screenshot_base: bytes = None) -> Image:
        """
        Get Image object with scaled screenshot of current screenshot
        iOS: Take driver screenshot and crop manually element from it

        :return: PIL Image object
        """
        if self.driver_wrapper.is_ios:
            element_box = self._element_box()
            window_height = self.driver.get_window_size()['height']
            image = self.driver_wrapper.screenshot_image()

            if window_height > self.size.height:
                image = image.crop(element_box)

        else:
            image = CoreElement.screenshot_image(self, screenshot_base)

        return image

    @property
    def size(self) -> Size:
        """
        Get Size object of current element

        :return: Size(width/height) obj
        """
        if self.driver_wrapper.is_native_context:
            return Size(**self.element.size)

        return CoreElement.size.fget(self)

    @property
    def location(self) -> Location:
        """
        Get Location object of current element

        :return: Location(x/y) obj
        """
        if self.driver_wrapper.is_native_context:
            return Location(**self.element.location)

        return CoreElement.location.fget(self)

    def _element_box(self) -> tuple:
        """
        Get element coordinates on screen for ios safari

        :return: element coordinates on screen (start_x, start_y, end_x, end_y)
        """
        element_size = self.size
        element_location = self.location

        return (
            element_location.x,
            element_location.y,
            element_location.x + element_size.width,
            element_location.y + element_size.height,
        )
