from __future__ import annotations

from copy import copy
from typing import Union, List, Type, Tuple, Optional

from PIL.Image import Image
from dyatel.mixins.objects.wait_result import Result
from playwright.sync_api import Page as PlaywrightDriver
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver

from dyatel.abstraction.element_abc import ElementABC
from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.exceptions import *
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object, DriverMixin
from dyatel.mixins.internal_mixin import InternalMixin, get_element_info
from dyatel.mixins.objects.cut_box import CutBox
from dyatel.mixins.objects.locator import Locator
from dyatel.mixins.objects.size import Size
from dyatel.utils.logs import Logging, LogLevel
from dyatel.utils.previous_object_driver import PreviousObjectDriver, set_instance_frame
from dyatel.visual_comparison import VisualComparison
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.utils.internal_utils import (
    WAIT_EL,
    is_target_on_screen,
    initialize_objects,
    get_child_elements_with_names,
    safe_getattribute,
    set_parent_for_attr,
    is_page,
    QUARTER_WAIT_EL,
    wait_condition,
)


class Element(DriverMixin, InternalMixin, Logging, ElementABC):
    """ Element object crossroad. Should be defined as Page/Group class variable """

    _object = 'element'
    _base_cls: Type[PlayElement, MobileElement, WebElement]
    driver_wrapper: DriverWrapper

    def __new__(cls, *args, **kwargs):
        instance = super(Element, cls).__new__(cls)
        set_instance_frame(instance)
        return instance

    def __repr__(self):
        return self._repr_builder()

    def __call__(self, driver_wrapper: DriverWrapper = None):
        self.__full_init__(driver_wrapper=get_driver_wrapper_from_object(driver_wrapper))
        return self

    def __getattribute__(self, item):
        if 'element' in item and not safe_getattribute(self, '_initialized'):
            raise NotInitializedException(
                f'{repr(self)} object is not initialized. '
                'Try to initialize base object first or call it directly as a method'
            )

        return safe_getattribute(self, item)

    def __init__(
            self,
            locator: Union[Locator, str],
            name: str = '',
            parent: Union[Any, False] = None,
            wait: bool = None,
            driver_wrapper: Union[DriverWrapper, Any] = None,
    ):
        """
        Initializing of element based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of element. Can be defined without locator_type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Group or other Element objects or False for skip
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self._validate_inheritance()

        if parent:
            assert isinstance(parent, (bool, Element)), \
                f'The "parent" of "{self.name}" should take an Element/Group object or False for skip. Get {parent}'

        self.locator = locator
        self.name = name if name else locator
        self.parent = parent
        self.wait = wait
        self.driver_wrapper = get_driver_wrapper_from_object(driver_wrapper)

        self._init_locals = getattr(self, '_init_locals', locals())
        self._safe_setter('__base_obj_id', id(self))
        self._initialized = False

        if self.driver_wrapper:
            self.__full_init__(driver_wrapper)

    def __full_init__(self, driver_wrapper: Any = None):
        self._driver_wrapper_given = bool(driver_wrapper)

        if self._driver_wrapper_given and driver_wrapper != self.driver_wrapper:
            self.driver_wrapper = get_driver_wrapper_from_object(driver_wrapper)

        self._modify_object()
        self._modify_children()

        if not self._initialized:
            self.__init_base_class__()

    def __init_base_class__(self) -> None:
        """
        Initialise base class according to current driver, and set his methods

        :return: None
        """
        if isinstance(self.driver, PlaywrightDriver):
            self._base_cls = PlayElement
        elif isinstance(self.driver, AppiumDriver):
            self._base_cls = MobileElement
        elif isinstance(self.driver, SeleniumDriver):
            self._base_cls = WebElement
        else:
            raise DriverWrapperException(f'Cant specify {self.__class__.__name__}')

        self._set_static(self._base_cls)
        self._base_cls.__init__(self, locator=self.locator)
        self._initialized = True

    # Following methods works same for both Selenium/Appium and Playwright APIs using internal methods

    # Elements interaction

    def set_text(self, text: str, silent: bool = False) -> Element:
        """
        Set (clear and type) text in current element

        :param text: text to be filled
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Set text in "{self.name}"')

        self.clear_text(silent=True).type_text(text, silent=True)
        return self

    def send_keyboard_action(self, action: Union[str, KeyboardKeys]) -> Element:
        """
        Send keyboard action to current element

        :param action: keyboard action
        :return: self
        """
        if self.driver_wrapper.is_playwright:
            self.click()
            self.driver.keyboard.press(action)
        else:
            self.type_text(action)

        return self

    # Elements waits

    def wait_visibility_without_error(self, *, timeout: Union[int, float] = QUARTER_WAIT_EL, silent: bool = False) -> Element:
        """
        Wait until element visibility without error

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" becomes visible without error exception')

        try:
            self.wait_visibility(timeout=timeout, silent=True)
        except (TimeoutException, WebDriverException) as exception:
            if not silent:
                self.log(f'Ignored exception: "{exception.msg}"')
        return self

    def wait_hidden_without_error(
            self,
            *,
            timeout: Union[int, float] = QUARTER_WAIT_EL,
            silent: bool = False
    ) -> Element:
        """
        Wait until element hidden without error

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" becomes hidden without error exception')

        try:
            self.wait_hidden(timeout=timeout, silent=True)
        except (TimeoutException, WebDriverException) as exception:
            if not silent:
                self.log(f'Ignored exception: "{exception.msg}"')
        return self

    @wait_condition
    def wait_for_text(
            self,
            expected_text: Optional[str] = None,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> Element:
        """
        Wait given or non-empty text presence in element

        :param expected_text: text to be waiting for. None or empty for any text
        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        actual_text = self.text

        if expected_text:
            result = actual_text == expected_text
            error = f'Not expected text for "{self.name}"'
            log_msg = f'Wait until text of "{self.name}" will be equal to "{expected_text}"'
        else:
            result = actual_text
            error = f'Text of "{self.name}" is empty'
            log_msg = f'Wait for any text of "{self.name}"'

        return Result(result, log_msg, UnexpectedTextException(error, actual_text, expected_text))  # noqa

    @wait_condition
    def wait_for_value(
            self,
            expected_value: Optional[str] = None,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> Element:
        """
        Wait given or non-empty value presence in element

        :param expected_value: value to be waiting for. :obj:`None` - any value; :class:`str` - expected value
        :param timeout: wait timeout
        :param silent: erase log
        :return: :class:`Element`
        """
        actual_value = self.value

        if expected_value:
            result = actual_value == expected_value
            error = f'Not expected value for "{self.name}"'
            log_msg = f'Wait until value of "{self.name}" will be equal to "{expected_value}"'
        else:
            result = actual_value
            error = f'Value of "{self.name}" is empty'
            log_msg = f'Wait for any value inside "{self.name}"'

        return Result(result, log_msg, UnexpectedValueException(error, actual_value, expected_value))  # noqa

    @wait_condition
    def wait_enabled(self, *, timeout: Union[int, float] = WAIT_EL, silent: bool = False) -> Element:
        """
        Wait until element clickable

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        return Result(  # noqa
            execution_result=self.is_enabled(silent=True),
            log=f'Wait until "{self.name}" becomes enabled',
            exc=TimeoutException(f'"{self.name}" is not enabled', info=self),
        )

    @wait_condition
    def wait_disabled(self, *, timeout: Union[int, float] = WAIT_EL, silent: bool = False) -> Element:
        """
        Wait until element disabled

        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        return Result(  # noqa
            execution_result=not self.is_enabled(silent=True),
            log=f'Wait until "{self.name}" becomes disabled',
            exc=TimeoutException(f'"{self.name}" is not disabled', info=self),
        )

    @wait_condition
    def wait_for_size(
            self,
            expected_size: Size,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> Element:
        """
        Wait until element size will be equal to given Size object

        :param expected_size: expected element size in Size object
        :param timeout: time to stop waiting
        :param silent: erase log
        :return: self
        """
        actual = self.size
        is_height_equal = actual.height == expected_size.height if expected_size.height is not None else True
        is_width_equal = actual.width == expected_size.width if expected_size.width is not None else True
        return Result(  # noqa
            execution_result=is_height_equal and is_width_equal,
            log=f'Wait until "{self.name}" size will be equal to {expected_size}',
            exc=UnexpectedElementSizeException(f'Unexpected size for "{self.name}"', actual, expected_size),
        )

    @wait_condition
    def wait_elements_count(
            self,
            expected_count: int,
            *,
            timeout: Union[int, float] = WAIT_EL,
            silent: bool = False
    ) -> Element:
        """
        Wait until elements count will be equal to expected value

        :param expected_count: expected elements count
        :param timeout: wait timeout
        :param silent: erase log
        :return: self
        """
        actual_count = self.get_elements_count(silent=True)
        error_msg = f'Unexpected elements count of "{self.name}"'
        return Result(  # noqa
            execution_result=actual_count == expected_count,
            log=f'Wait until elements count of "{self.name}" will be equal to "{expected_count}"',
            exc=UnexpectedElementsCountException(error_msg, actual_count, expected_count),
        )


    @property
    def all_elements(self) -> List[Element]:
        if getattr(self, '_wrapped', None):
            raise RecursionError(f'all_elements property already used for {self.name}')

        return self._base_cls.all_elements.fget(self)

    def is_visible(self, silent: bool = False, check_displaying: bool = True) -> bool:
        """
        Check is current element top left corner or bottom right corner visible on current screen

        :param silent: erase log
        :param check_displaying: trigger is_displayed additionally
        :return: :class:`bool`
        """
        if not silent:
            self.log(f'Check visibility of "{self.name}"')

        is_visible = True

        if check_displaying:
            is_visible = self.is_displayed()

        if is_visible:
            rect, window_size = self.get_rect(), self.driver_wrapper.get_inner_window_size()
            x_end, y_end = rect['x'] + rect['width'], rect['y'] + rect['height']
            is_start_visible = is_target_on_screen(x=rect['x'], y=rect['y'], possible_range=window_size)
            is_end_visible = is_target_on_screen(x=x_end, y=y_end, possible_range=window_size)
            is_visible = is_start_visible or is_end_visible

        return is_visible

    def is_fully_visible(self, silent: bool = False, check_displaying: bool = True) -> bool:
        """
        Check is current element top left corner and bottom right corner visible on current screen

        :param silent: erase log
        :param check_displaying: If `True`, the :func:`is_displayed` method will be called additionally.
          The checking process will stop if this method returns `False`.
        :return: :class:`bool`
        """
        if not silent:
            self.log(f'Check fully visibility of "{self.name}"')

        is_visible = True

        if check_displaying:
            is_visible = self.is_displayed()

        if is_visible:
            rect, window_size = self.get_rect(), self.driver_wrapper.get_inner_window_size()
            x_end, y_end = rect['x'] + rect['width'], rect['y'] + rect['height']
            is_start_visible = is_target_on_screen(x=rect['x'], y=rect['y'], possible_range=window_size)
            is_end_visible = is_target_on_screen(x=x_end, y=y_end, possible_range=window_size)
            is_visible = is_start_visible and is_end_visible

        return is_visible

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
        self.log(f'Save screenshot of {self.name}')

        image_object = screenshot_base
        if type(screenshot_base) is bytes:
            image_object = self._base_cls.screenshot_image(self, screenshot_base)

        if convert_type:
            image_object = image_object.convert(convert_type)

        image_object.save(file_name)

        return image_object

    def hide(self) -> Element:
        """
        Hide current element from page

        :return: self
        """
        self.execute_script('arguments[0].style.opacity = "0";')
        return self

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute script using current element

        :param script: js script, that have `arguments[0]`
        :param args: any other args for `arguments[1]` `arguments[2]` etc.
        :return: Any
        """
        return self.driver_wrapper.execute_script(script, *[self, *[arg for arg in args]])

    def assert_screenshot(
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
        :param hide: hide elements from page before taking screenshot
        :param fill_background: fill background with given color or black color by default
        :param cut_box: custom coordinates, that will be cut from original image (left, top, right, bottom)
        :return: None
        """
        delay = delay or VisualComparison.default_delay
        remove = [remove] if type(remove) is not list and remove else remove

        if hide:
            if not isinstance(hide, list):
                hide = [hide]
            for object_to_hide in hide:
                object_to_hide.hide()

        VisualComparison(self.driver_wrapper, self).assert_screenshot(
            filename=filename, test_name=test_name, name_suffix=name_suffix, threshold=threshold, delay=delay,
            scroll=scroll, remove=remove, fill_background=fill_background, cut_box=cut_box
        )

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
        try:
            self.assert_screenshot(
                filename, test_name, name_suffix, threshold, delay, scroll, remove, fill_background, cut_box, hide
            )
        except AssertionError as exc:
            exc = str(exc)
            self.log(exc, level=LogLevel.ERROR)
            return False, exc

        return True, f'No visual mismatch found for {self.name}'

    def get_element_info(self, element: Element = None) -> str:
        """
        Get full loging data depends on parent element

        :param element: element to collect log data
        :return: log string
        """
        element = element if element else self
        return get_element_info(element)

    def _get_all_elements(self, sources: Union[tuple, list]) -> List[Any]:
        """
        Get all wrapped elements from sources

        :param sources: list of elements: `all_elements` from selenium or `element_handles` from playwright
        :return: list of wrapped elements
        """
        wrapped_elements = []

        for element in sources:
            wrapped_object: Any = copy(self)
            wrapped_object.element = element
            wrapped_object._wrapped = True
            set_parent_for_attr(wrapped_object, Element, with_copy=True)
            wrapped_elements.append(wrapped_object)

        return wrapped_elements

    def _modify_children(self):
        """
        Initializing of attributes with  type == Element.
        Required for classes with base == Element.
        """
        initialize_objects(self, get_child_elements_with_names(self, Element), Element)

    def _modify_object(self):
        """
        Modify current object if driver_wrapper is not given. Required for Page that placed into functions:
        - sets driver from previous object
        """
        if not self._driver_wrapper_given:
            PreviousObjectDriver().set_driver_from_previous_object(self)

    def _validate_inheritance(self):
        cls = self.__class__
        mro = cls.__mro__

        for item in mro:
            if is_page(item):
                raise TypeError(
                    f"You cannot make an inheritance for {cls.__name__} from both Element/Group and Page objects")
