from logging import info

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement


class WebElement(CoreElement):

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver: SeleniumWebDriver = CoreDriver.driver
        super(WebElement, self).__init__(locator=locator, locator_type=locator_type, name=name, parent=parent)

    def click(self):
        info(f'Click into "{self.name}"')
        self.wait_element(silent=True).element.click()
        return self

    def hover(self):
        info(f'Hover over {self.name}')
        ActionChains(self.driver)\
            .move_to_element(self.element)\
            .move_by_offset(1, 1)\
            .move_to_element(self.element)\
            .perform()
        return self

    def click_outside(self, x=-1, y=-1):
        self.wait_element(silent=True)
        dx, dy = self.calculate_coordinate_to_click(self.element, x, y)
        ActionChains(self.driver).move_to_element_with_offset(self.element, dx, dy).click().perform()
        return self

    def calculate_coordinate_to_click(self, element, x, y):
        """
            calculate coordinates to click from element
            :param element: element to calculate tap from
            :param x: horizontal offset relative to either left (x < 0) or right side (x > 0)
            :param y: vertical offset relative to either top (y > 0) or bottom side (y < 0)
            Examples:
                * (0, 0) -- center of the element
                * (5, 0) -- 5 pixels to the right
                * (-10, 0) -- 10 pixels to the left
                * (0, -5) -- 5 pixels below
                * (0, 10) -- 10 pixels above
        """
        half_width, half_height = element.size['width'] / 2, element.size['height'] / 2
        dx, dy = half_width, half_height
        if x:
            dx += x + (-half_width if x < 0 else half_width)
        if y:
            dy += -y + (half_height if y < 0 else -half_height)
        return dx, dy
