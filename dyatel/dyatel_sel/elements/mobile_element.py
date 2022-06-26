from logging import info

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.internal_utils import calculate_coordinate_to_click


class MobileElement(CoreElement):

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver: AppiumWebDriver = CoreDriver.driver
        CoreElement.__init__(self, locator=locator, locator_type=locator_type, name=name, parent=parent)

    @property
    def all_elements(self) -> list:
        """
        Get all MobileElement elements, matching given locator

        :return: list of elements
        """
        wrapped_elements = []
        for element in self._get_driver().find_elements(self.locator_type, self.locator):
            wrapped_object = MobileElement(self.locator, self.locator_type, self.name, self.parent)
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

    def click_outside(self, x=0, y=-5):
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

    def get_screenshot(self, filename, legacy=True):
        if self.driver_wrapper.is_ios and legacy:
            element_box = self.element_box()
            window_width = self.driver.get_window_size()['width']
            img_binary = self.driver_wrapper.driver.get_screenshot_as_png()  # FIXME
            scaled_image = self.scaled_screenshot(img_binary, window_width)
            image_binary = scaled_image.crop(element_box)
            image_binary.save(filename)
        else:
            image_binary = super().get_screenshot(filename)

        return image_binary
