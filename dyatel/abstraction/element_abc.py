from __future__ import annotations

from abc import ABC
from typing import Union, Any, List, Tuple, Optional, TYPE_CHECKING

from PIL.Image import Image
from appium.webdriver.extensions.location import Location
from dyatel.mixins.objects.cut_box import CutBox
from dyatel.mixins.objects.scrolls import ScrollTo, ScrollTypes
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.webelement import WebElement as AppiumWebElement
from playwright.sync_api import Locator as PlayWebElement

from dyatel.abstraction.mixin_abc import MixinABC
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.mixins.objects.size import Size
from dyatel.utils.internal_utils import WAIT_EL, QUARTER_WAIT_EL

if TYPE_CHECKING:
    from dyatel.base.element import Element  # Import the concrete class for documentation purposes


class ElementABC(MixinABC, ABC):

    locator: str = None
    locator_type: str = None
    name: str = None
    parent: Optional["Element"] = None
    wait: bool = None

    @property
    def element(self) -> Union[SeleniumWebElement, AppiumWebElement, PlayWebElement]:
        """
        Get a web element object depending on current driver

        :return: Union[:class:`~selenium.webdriver.remote.webelement.WebElement`, :class:`AppiumWebElement`, :class:`PlayWebElement`]
        """
        raise NotImplementedError()

    @element.setter
    def element(self, base_element: Union[SeleniumWebElement, AppiumWebElement, PlayWebElement]):
        """
        Element object setter. Try to avoid usage of this function

        :param base_element: Union[:class:`SeleniumWebElement`, :class:`AppiumWebElement`, :class:`PlayWebElement`]
        """
        raise NotImplementedError()

    @property
    def all_elements(self) -> Union[list, List["Element"]]:
        """
        Get all wrapped elements with different source objects

        :return: :class:`list` [:class:`Element`] - list of wrapped objects
        """
        raise NotImplementedError()

    def click(self, force_wait: bool = True, *args, **kwargs) -> "Element":
        """
        Click to current element

        :param force_wait: wait for element visibility before click

        **Selenium/Appium:**

        :param args: compatibility arg for playwright
        :param kwargs: compatibility arg for playwright

        **Playwright:**

        :param args: `any args params <https://playwright.dev/python/docs/api/class-locator#locator-click>`_
        :param kwargs: `any kwargs params <https://playwright.dev/python/docs/api/class-locator#locator-click>`_
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def click_into_center(self, silent: bool = False) -> "Element":
        """
        Click into the center of element

        :param silent: erase log message
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def type_text(self, text: Union[str, KeyboardKeys], silent: bool = False) -> "Element":
        """
        Type text to current element

        :param text: text to be typed
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def type_slowly(self, text: str, sleep_gap: float = 0.05, silent: bool = False) -> "Element":
        """
        Type text to current element slowly

        :param text: text to be slowly typed
        :param sleep_gap: sleep gap before each key press
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def clear_text(self, silent: bool = False) -> "Element":
        """
        Clear text from current element

        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def check(self) -> "Element":
        """
        Check current checkbox

        :return: :class:`Element`
        """
        raise NotImplementedError()

    def uncheck(self) -> "Element":
        """
        Uncheck current checkbox

        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_visibility(self, *, timeout: int = WAIT_EL, silent: bool = False) -> "Element":
        """
        Wait for current element available in page

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_hidden(self, *, timeout: int = WAIT_EL, silent: bool = False) -> "Element":
        """
        Wait until current element hidden

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_availability(self, *, timeout: int = WAIT_EL, silent: bool = False) -> "Element":
        """
        Wait for current element available in DOM

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def save_screenshot(
            self,
            file_name: str,
            screenshot_base: Union[bytes, Image] = None,
            convert_type: str = None
    ) -> Image:
        """
        Takes element screenshot and saving with given path/filename

        :param file_name: path/filename
        :param screenshot_base: use given image binary instead of taking a new screenshot
        :param convert_type: convert image type before save
        :return: PIL Image object
        """
        raise NotImplementedError()

    def hide(self) -> "Element":
        """
        Hide current element from page

        :return: :class:`Element`
        """
        raise NotImplementedError()

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute script using current element

        :param script: js script, that have `arguments[0]`
        :param args: any other args for `arguments[1]` `arguments[2]` etc.
        :return: :class:`Any`
        """
        raise NotImplementedError()

    def screenshot_image(self, screenshot_base: bytes = None) -> Image:
        """
        Get PIL Image object with scaled screenshot of current element

        :param screenshot_base: screenshot bytes
        :return: PIL :class:`Image` object
        """
        raise NotImplementedError()

    @property
    def screenshot_base(self) -> bytes:
        """
        Get screenshot binary of current element

        :return: :class:`bytes` - screenshot binary
        """
        raise NotImplementedError()

    @property
    def text(self) -> str:
        """
        Get text from current element

        :return: :class:`str` - element text
        """
        raise NotImplementedError()

    @property
    def inner_text(self) -> str:
        """
        Get current element inner text

        :return: :class:`str` - element inner text
        """
        raise NotImplementedError()

    @property
    def value(self) -> str:
        """
        Get value from current element

        :return: :class:`str` - element value
        """
        raise NotImplementedError()

    def is_available(self) -> bool:
        """
        Check current element availability in DOM

        :return: :class:`bool` - True if present in DOM
        """
        raise NotImplementedError()

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of element

        :param silent: erase log
        :return: :class:`bool` - True if element visible
        """
        raise NotImplementedError()

    def is_hidden(self, silent: bool = False) -> bool:
        """
        Check invisibility of current element

        :param silent: erase log
        :return: :class:`bool` - True if element hidden
        """
        raise NotImplementedError()

    def get_attribute(self, attribute: str, silent: bool = False) -> str:
        """
        Get custom attribute from current element

        :param attribute: custom attribute: value, innerText, textContent etc.
        :param silent: erase log
        :return: :class:`str` - custom attribute value
        """
        raise NotImplementedError()

    def get_all_texts(self, silent: bool = False) -> List[str]:
        """
        Get all texts from all matching elements

        :param silent: erase log
        :return: :class:`list` [:class:`str`] - text content from all matching elements
        """
        raise NotImplementedError()

    def get_elements_count(self, silent: bool = False) -> int:
        """
        Get elements count

        :param silent: erase log
        :return: :class:`int`
        """
        raise NotImplementedError()

    def get_rect(self) -> dict:
        """
        A dictionary with the size and location of the element.

        :return: :class:`dict` ~ {'y': 0, 'x': 0, 'width': 0, 'height': 0}
        """
        raise NotImplementedError()

    @property
    def size(self) -> Size:
        """
        Get Size object of current element

        :return: Size(width/height) obj
        """
        raise NotImplementedError()

    @property
    def location(self) -> Location:
        """
        Get Location object of current element

        :return: Location(x/y) obj
        """
        raise NotImplementedError()

    def is_enabled(self, silent: bool = False) -> bool:
        """
        Check if element enabled

        :param silent: erase log
        :return: :class:`bool` True if element enabled
        """
        raise NotImplementedError()

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: :class:`bool`
        """
        raise NotImplementedError()

    def hover(self, silent: bool = False) -> "Element":
        """
        Hover over current element

        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def hover_outside(self, x: int = 0, y: int = -5) -> "Element":
        """
        Hover outside from current element. By default, 5px above  of element

        :param x: x-offset of element to hover
        :param y: y-offset of element to hover
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def click_outside(self, x: int = -1, y: int = -1) -> "Element":
        """
        Click outside of element. By default, 1px above and 1px left of element

        :param x: x offset of element to click
        :param y: y offset of element to click
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def click_in_alert(self) -> "Element":
        """
        Mobile only:
        Click on element in alert with switch to native context

        :return: :class:`Element`
        """
        raise NotImplementedError()

    def set_text(self, text: str, silent: bool = False) -> "Element":
        """
        Set (clear and type) text in current element

        :param text: text to be filled
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def send_keyboard_action(self, action: Union[str, KeyboardKeys]) -> "Element":
        """
        Send keyboard action to current element

        :param action: keyboard action
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_elements_count(
            self,
            expected_count: int,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait until elements count will be equal to expected value

        :param expected_count: expected elements count
        :param timeout: wait timeout
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_for_text(
            self,
            expected_text: Optional[str] = None,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait given or non-empty text presence in element

        :param expected_text: text to be waiting for. None or empty for any text
        :param timeout: wait timeout
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_for_value(
            self,
            expected_value: Optional[str] = None,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait given or non-empty value presence in element

        :param expected_value: value to be waiting for. :obj:`None` - any value; :class:`str` - expected value
        :param timeout: wait timeout
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_visibility_without_error(
            self,
            *,
            timeout: [int, float] = QUARTER_WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait until element visibility without error

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_hidden_without_error(
            self,
            *,
            timeout: [int, float] = QUARTER_WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait until element hidden without error

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_enabled(self, *, timeout: [int, float] = WAIT_EL, silent: bool = False) -> "Element":
        """
        Wait until element clickable

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_disabled(self, *, timeout: [int, float] = WAIT_EL, silent: bool = False) -> "Element":
        """
        Wait until element clickable

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def wait_for_size(
            self,
            *,
            expected_size: Size,
            timeout: [int, float] = WAIT_EL,
            silent: bool = False
    ) -> "Element":
        """
        Wait until element size will be equal to given Size object

        :param expected_size: :class:`Size` object - expected element
        :param timeout: time to stop waiting
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def is_visible(self, silent: bool = False, check_displaying: bool = True) -> bool:
        """
        Check is current element top left corner or bottom right corner visible on current screen

        :param silent: erase log
        :param check_displaying: If `True`, the :func:`is_displayed` method will be called additionally.
          The checking process will stop if this method returns `False`.
        :return: :class:`bool`
        """
        raise NotImplementedError()

    def is_fully_visible(self, silent: bool = False, check_displaying: bool = True) -> bool:
        """
        Check is current element top left corner and bottom right corner visible on current screen

        :param silent: erase log
        :param check_displaying: If `True`, the :func:`is_displayed` method will be called additionally.
          The checking process will stop if this method returns `False`.
        :return: :class:`bool`
        """
        raise NotImplementedError()

    def scroll_into_view(
            self,
            block: ScrollTo = ScrollTo.CENTER,
            behavior: ScrollTypes = ScrollTypes.INSTANT,
            sleep: Union[int, float] = 0,
            silent: bool = False,
    ) -> "Element":
        """
        Scroll element into view by js script

        :param block: one of :class:`ScrollTo` object
        :param behavior: one of :class:`ScrollTypes` object
        :param sleep: delay after scroll
        :param silent: erase log
        :return: :class:`Element`
        """
        raise NotImplementedError()

    def assert_screenshot(
            self,
            filename: str = '',
            test_name: str = '',
            name_suffix: str = '',
            threshold: Union[int, float] = None,
            delay: Union[int, float] = None,
            scroll: bool = False,
            remove: Union[ElementABC, List[ElementABC]] = None,
            fill_background: Union[str, bool] = False
    ) -> None:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/negative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :param remove: remove elements from screenshot
        :param fill_background: fill background with given color or black color by default
        :return: :class:`None`
        """
        raise NotImplementedError()

    def soft_assert_screenshot(
            self,
            filename: str = '',
            test_name: str = '',
            name_suffix: str = '',
            threshold: Union[int, float] = None,
            delay: Union[int, float] = None,
            scroll: bool = False,
            remove: Union[Element, List[Element]] = None,
            fill_background: Union[str, bool] = False,
            cut_box: CutBox = None,
            hide: Union[Element, List[Element]] = None,
    ) -> Tuple[bool, str]:
        """
        Soft assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/negative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param scroll: scroll to element before taking the screenshot
        :param remove: remove elements from screenshot
        :param hide: hide elements from page before taking screenshot
        :param fill_background: fill background with given color or black color by default
        :param cut_box: :class:`CutBox` - custom coordinates, that will be cut from original image
        :return: :class:`bool` - :obj:`True`: screenshots equal; :obj:`False`: screenshots mismatch;
        """
        raise NotImplementedError()

    def get_element_info(self, element: Optional["Element"] = None) -> str:
        """
        Get full loging data depends on parent element

        :param element: element to collect log data
        :return: :class:`str` - log string
        """
        raise NotImplementedError()

    def _get_all_elements(self, sources: Union[tuple, list]) -> List["Element"]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :return: :class:`list` [:class:`Element`] - list of wrapped elements
        """
        raise NotImplementedError()
