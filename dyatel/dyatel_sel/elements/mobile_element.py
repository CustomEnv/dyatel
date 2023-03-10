from __future__ import annotations

from typing import Union, List, BinaryIO, Any

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.mixins.core_mixin import calculate_coordinate_to_click
from dyatel.js_scripts import get_element_position_on_screen_js
from dyatel.mixins.locator_mixin import get_platform_locator, get_selenium_locator_type, get_appium_selector


class MobileElement(CoreElement):

    def __init__(self, locator: str, locator_type: str, name: str, parent: Union[MobileElement, Any], wait: bool):
        """
        Initializing of mobile element with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be MobileElement, MobilePage, Group objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        locator = get_platform_locator(self, default_locator=locator)
        locator_type = locator_type if locator_type else get_selenium_locator_type(locator)
        locator, locator_type = get_appium_selector(locator, locator_type)

        CoreElement.__init__(
            self,
            locator=locator,
            locator_type=locator_type,
            name=name,
            parent=parent,
            wait=wait
        )

    @property
    def all_elements(self) -> Union[None, List[Any]]:
        """
        Get all wrapped elements with appium bases

        :return: list of wrapped objects
        """
        appium_elements = self._find_elements(self._get_base())
        return self._get_all_elements(appium_elements, MobileElement)

    def click_outside(self, x: int = 0, y: int = -5, calculate_top_bar=True) -> MobileElement:
        """
        Click outside of element. By default, 5px above  of element

        :param x: x offset of element to tap
        :param y: y offset of element to tap
        :param calculate_top_bar: iOS only - attach top bar height to calculation
        :return: self
        """
        if self.driver_wrapper.is_web_context:
            if not self.is_fully_visible(silent=True):
                self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, x, y)

        if calculate_top_bar and self.driver_wrapper.is_ios:
            y += self.driver_wrapper.get_top_bar_height()

        self.log(f'Tap outside from "{self.name}" with coordinates (x: {x}, y: {y})')

        self.driver_wrapper.click_by_coordinates(x=x, y=y, silent=True)
        return self

    def click_into_center(self, calculate_top_bar: bool = True, silent: bool = True) -> MobileElement:
        """
        Click into the center of element

        :param calculate_top_bar: iOS only - attach top bar height to calculation
        :param silent: erase log message
        :return: self
        """
        if self.driver_wrapper.is_web_context:
            if not self.is_fully_visible(silent=True):
                self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, 0, 0)

        if calculate_top_bar and self.driver_wrapper.is_ios:
            y += self.driver_wrapper.get_top_bar_height()

        if not silent:
            self.log(f'Tap into the center by coordinates (x: {x}, y: {y}) for "{self.name}"')

        self.driver_wrapper.click_by_coordinates(x, y, silent=True)

        return self

    def hover(self, calculate_top_bar: bool = True, silent: bool = False) -> MobileElement:
        """
        Hover over current element

        :param calculate_top_bar: iOS only - attach top bar height to calculation
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Hover over "{self.name}"')

        self.click_into_center(calculate_top_bar=calculate_top_bar)
        return self

    def hover_outside(self, x: int = 0, y: int = -5, calculate_top_bar=True) -> MobileElement:
        """
        Hover outside from current element. By default, 5px above  of element

        :param x: x-offset of element to hover(tap)
        :param y: y-offset of element to hover(tap)
        :param calculate_top_bar: iOS only - attach top bar height to calculation
        :return: self
        """
        return self.click_outside(x=x, y=y, calculate_top_bar=calculate_top_bar)

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

    def _element_box(self) -> tuple:
        """
        Get element coordinates on screen for ios safari

        :return: element coordinates on screen (start_x, start_y, end_x, end_y)
        """
        element = self.element
        el_location = self.driver.execute_script(get_element_position_on_screen_js, element)
        start_x, start_y = el_location.values()
        h, w = element.size.values()

        bar_size = self.driver_wrapper.get_top_bar_height()

        if bar_size:
            start_y += bar_size

        return start_x, start_y, start_x+w, start_y+h
