import os
from io import BytesIO
from typing import Union

from PIL import Image
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.webelement import WebElement as AppiumWebElement

from dyatel.visual_comparison import assert_same_images


def get_child_elements(self, instance):
    """Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements = []

    class_items = list(self.__dict__.items()) + list(self.__class__.__dict__.items())

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    for attribute, value in class_items:
        if isinstance(value, instance):
            elements.append(value)
    return set(elements)


def get_timeout(timeout):
    if timeout < 100:  # for timeout in ms
        timeout *= 1000
    return timeout


def calculate_coordinate_to_click(element, x, y):
    """
    Calculate coordinates to click for element
    Examples:
        (0, 0) -- center of the element
        (5, 0) -- 5 pixels to the right
        (-10, 0) -- 10 pixels to the left out of the element
        (0, -5) -- 5 pixels below the element

    :param element: dyatel WebElement or MobileElement
    :param x: horizontal offset relative to either left (x < 0) or right side (x > 0)
    :param y: vertical offset relative to either top (y > 0) or bottom side (y < 0)
    :return:  coordinates
    """
    element_size = element.element.size
    half_width, half_height = element_size['width'] / 2, element_size['height'] / 2
    dx, dy = half_width, half_height
    if x:
        dx += x + (-half_width if x < 0 else half_width)
    if y:
        dy += -y + (half_height if y < 0 else -half_height)
    return dx, dy


class AfterInitMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.after_init()
        return obj


class Mixin:
    driver = None
    parent = None
    locator: str = None
    locator_type: str = None
    element: Union[SeleniumWebElement, AppiumWebElement] = None
    scroll_into_view = None
    get_screenshot = None

    def get_element_logging_data(self, element=None) -> str:
        element = element if element else self
        parent = element.parent
        current_data = f'Selector: ["{element.locator_type}": "{element.locator}"]'
        if parent:
            parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
            current_data = f'{current_data}. {parent_data}'
        return current_data

    def scaled_screenshot(self, screenshot_binary, element_width) -> Image:
        img_binary = Image.open(BytesIO(screenshot_binary))
        scale = img_binary.size[0] / element_width

        if scale != 1:
            new_image_size = (int(img_binary.size[0] / scale), int(img_binary.size[1] / scale))
            img_binary = img_binary.resize(new_image_size, Image.ANTIALIAS)

        return img_binary

    def element_box(self) -> tuple:
        self.scroll_into_view(sleep=0.1)

        start_x, start_y = self.get_element_position_on_screen().values()
        h, w = self.element.size.values()

        inner_height = self.driver.execute_script('return window.innerHeight')
        outer_height = self.driver.execute_script('return window.outerHeight')
        bars_size = outer_height - inner_height

        if bars_size > 110:  # FIXME: magick value
            bar_size = bars_size / 4
        else:
            bar_size = bars_size / 2

        if bar_size:
            start_y += bar_size

        return start_x, start_y, start_x+w, start_y+h

    def get_element_position_on_screen(self) -> dict:
        get_element_position_on_screen = """
        function getPositionOnScreen(elem) {
          let box = elem.getBoundingClientRect();
          var y;
          var x;
          y = Math.floor(box.top)
          x = Math.floor(box.left)
          return {
            x: x,
            y: y
          };
        };
        return getPositionOnScreen(arguments[0])
        """
        return self.driver.execute_script(get_element_position_on_screen, self.element)

    def assert_screenshot(self, filename, threshold=0):
        root_path = os.environ.get('visual', '')
        reference_file = f'{root_path}/reference/{filename}.png'

        try:
            Image.open(reference_file)
        except FileNotFoundError:
            self.get_screenshot(reference_file)
            message = 'Reference file not found, but its just saved. ' \
                      'If it CI run, then you need to commit reference files.'
            raise FileNotFoundError(message) from None

        output_file = f'{root_path}/output/{filename}.png'
        self.get_screenshot(output_file)
        assert_same_images(output_file, reference_file, filename, threshold)
