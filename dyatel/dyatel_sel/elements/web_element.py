from logging import info

from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.internal_utils import calculate_coordinate_to_click


class WebElement(CoreElement):

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        CoreElement.__init__(self, locator=locator, locator_type=locator_type, name=name, parent=parent)

    @property
    def all_elements(self) -> list:
        """
        Get all WebElement elements, matching given locator

        :return: list of elements
        """
        wrapped_elements = []
        for element in self._get_driver().find_elements(self.locator_type, self.locator):
            wrapped_object = WebElement(self.locator, self.locator_type, self.name, self.parent)
            wrapped_object.element = element
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    def hover(self):
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

    def click_outside(self, x=-1, y=-1):
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
