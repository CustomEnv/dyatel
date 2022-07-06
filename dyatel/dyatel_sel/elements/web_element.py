from __future__ import annotations

from logging import info
from typing import Union, List, Any

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.internal_utils import calculate_coordinate_to_click


class WebElement(CoreElement):
    def __init__(self, locator: str, locator_type='', name='',
                 parent: Union[WebElement, Any] = None, wait=False):
        """
        Initializing of web element with selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be WebElement, WebPage, Group objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        CoreElement.__init__(self, locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    @property
    def all_elements(self) -> List[Any]:
        """
        Get all wrapped elements with selenium bases

        :return: list of wrapped objects
        """
        selenium_elements = self._get_driver(wait=False).find_elements(self.locator_type, self.locator)
        return self._get_all_elements(selenium_elements, WebElement)

    def hover(self) -> WebElement:
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

    def click_outside(self, x=-1, y=-1) -> WebElement:
        """
        Click outside of element. By default, 1px above and 1px left of element

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
