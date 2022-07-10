from __future__ import annotations

from logging import info
from typing import Union, List, BinaryIO, Any

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.internal_utils import calculate_coordinate_to_click
from dyatel.js_scripts import get_element_position_on_screen_js


class MobileElement(CoreElement):

    def __init__(self, locator: str, locator_type='', name='',
                 parent: Union[MobileElement, Any] = None, wait=False):
        """
        Initializing of mobile element with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be MobileElement, MobilePage, Group objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        CoreElement.__init__(self, locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    @property
    def all_elements(self) -> List[Any]:
        """
        Get all wrapped elements with selenium bases

        :return: list of wrapped objects
        """
        appium_elements = self._get_driver(wait=False).find_elements(self.locator_type, self.locator)
        return self._get_all_elements(appium_elements, MobileElement)

    def hover(self) -> MobileElement:
        """
        Hover over current element

        :return: self
        """
        info(f'Hover over {self.name}')
        self._action_chains\
            .move_to_element(self.element)\
            .move_by_offset(1, 1)\
            .move_to_element(self.element)\
            .perform()
        return self

    def click_outside(self, x=0, y=-5) -> MobileElement:
        """
        Click outside of element. By default, 5px above  of element

        :param x: x offset
        :param y: y offset
        :return: self
        """
        self.wait_element(silent=True)
        dx, dy = calculate_coordinate_to_click(self, x, y)
        self._action_chains\
            .move_to_element_with_offset(self.element, dx, dy)\
            .click()\
            .perform()
        return self

    def get_screenshot(self, filename, legacy=True) -> BinaryIO:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :param legacy: iOS only - crop element for page screenshot manually
        :return: image binary
        """
        if self.driver_wrapper.is_ios and legacy:
            element_box = self._element_box()
            window_width = self.driver.get_window_size()['width']
            img_binary = self.driver_wrapper.driver.get_screenshot_as_png()  # FIXME
            scaled_image = self._scaled_screenshot(img_binary, window_width)
            image_binary = scaled_image.crop(element_box)
            image_binary.save(filename)
        else:
            image_binary = super().get_screenshot(filename)

        return image_binary

    def _element_box(self) -> tuple:
        """
        Get element coordinates on screen

        :return: element coordinates on screen (start_x, start_y, end_x, end_y)
        """
        self.scroll_into_view(sleep=0.1)

        el_location = self.driver.execute_script(get_element_position_on_screen_js, self.element)
        start_x, start_y = el_location.values()
        h, w = self.element.size.values()

        inner_height = self.driver.execute_script('return window.innerHeight')
        outer_height = self.driver.execute_script('return window.outerHeight')
        bars_size = outer_height - inner_height

        if bars_size > 110:  # FIXME: magick value
            bar_size = bars_size / 4  # top and bottom bar shown
        else:
            bar_size = bars_size / 2  # top bar shown

        if bar_size:
            start_y += bar_size

        return start_x, start_y, start_x+w, start_y+h
