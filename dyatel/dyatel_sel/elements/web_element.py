from __future__ import annotations

from abc import ABC
from typing import Union

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.mixins.objects.locator import take_locator_type, Locator
from dyatel.utils.internal_utils import calculate_coordinate_to_click
from dyatel.utils.selector_synchronizer import get_platform_locator, get_selenium_locator_type


class WebElement(CoreElement, ABC):

    def __init__(self, locator: Union[Locator, str]):
        """
        Initializing of web element with selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        """
        self.locator = get_platform_locator(self)
        self.locator_type = take_locator_type(locator) or get_selenium_locator_type(self.locator)

    def hover(self, silent: bool = False) -> WebElement:
        """
        Hover over current element

        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Hover over "{self.name}"')

        self._action_chains\
            .move_to_element(self.element)\
            .move_by_offset(1, 1)\
            .move_to_element(self.element)\
            .perform()
        return self

    def hover_outside(self, x: int = 0, y: int = -5) -> WebElement:
        """
        Hover outside from current element

        :param x: x-offset of element to hover
        :param y: y-offset of element to hover
        :return: self
        """
        self.log(f'Hover outside from "{self.name}"')

        if not self.is_fully_visible(silent=True):
            self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, x, y)
        self._action_chains\
            .move_to_location(x, y)\
            .perform()
        return self

    def click_outside(self, x: int = -1, y: int = -1) -> WebElement:
        """
        Click outside of element. By default, 1px above and 1px left of element

        :param x: x offset of element to click
        :param y: y offset of element to click
        :return: self
        """
        self.log(f'Click outside from "{self.name}"')

        if not self.is_fully_visible(silent=True):
            self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, x, y)

        self.driver_wrapper.click_by_coordinates(x=x, y=y, silent=True)
        return self

    def click_into_center(self, silent: bool = False) -> WebElement:
        """
        Click into the center of element

        :param silent: erase log message
        :return: self
        """
        if not self.is_fully_visible(silent=True):
            self.scroll_into_view()

        x, y = calculate_coordinate_to_click(self, 0, 0)

        if not silent:
            self.log(f'Click into the center (x: {x}, y: {y}) for "{self.name}"')

        self.driver_wrapper.click_by_coordinates(x=x, y=y, silent=True)
        return self
