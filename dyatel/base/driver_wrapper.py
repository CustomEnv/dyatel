from __future__ import annotations

from typing import Union, Type, List, Tuple, Any, Optional

from PIL import Image
from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumDriver
from playwright.sync_api import (
    Browser as PlaywrightBrowser,
    BrowserContext as PlaywrightContext,
    Page as PlaywrightDriver,
)

from dyatel.mixins.objects.cut_box import CutBox
from dyatel.visual_comparison import VisualComparison
from dyatel.abstraction.driver_wrapper_abc import DriverWrapperABC
from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.exceptions import DriverWrapperException
from dyatel.js_scripts import get_inner_height_js, get_inner_width_js
from dyatel.mixins.internal_mixin import InternalMixin
from dyatel.utils.internal_utils import get_attributes_from_object, get_child_elements_with_names
from dyatel.utils.logs import Logging, LogLevel


class DriverWrapperSessions:
    all_sessions: List[DriverWrapper] = []

    @classmethod
    def add_session(cls, driver_wrapper: DriverWrapper) -> None:
        """
        Add DriverWrapper object to pool

        :param driver_wrapper: DriverWrapper object
        :return: None
        """
        cls.all_sessions.append(driver_wrapper)

    @classmethod
    def remove_session(cls, driver_wrapper: DriverWrapper) -> None:
        """
        Remove DriverWrapper object from pool

        :param driver_wrapper: DriverWrapper object
        :return: None
        """
        cls.all_sessions.remove(driver_wrapper)

    @classmethod
    def sessions_count(cls) -> int:
        """
        Get initialised DriverWrapper objects count

        :return: number of sessions
        """
        return len(cls.all_sessions)

    @classmethod
    def first_session(cls) -> Union[DriverWrapper, None]:
        """
        Get first DriverWrapper object from pool

        :return: first DriverWrapper object or None
        """
        return cls.all_sessions[0] if cls.all_sessions else None

    @classmethod
    def is_connected(cls) -> bool:
        """
        Get connection status with any DriverWrapper object in pool

        :return: True if any DriverWrapper object is available
        """
        return any(cls.all_sessions)


class DriverWrapper(InternalMixin, Logging, DriverWrapperABC):
    """ Driver object crossroad """

    _object = 'driver_wrapper'
    _base_cls: Type[PlayDriver, MobileDriver, WebDriver] = None

    session: DriverWrapperSessions = DriverWrapperSessions

    anchor = None

    is_desktop = False
    is_selenium = False
    is_playwright = False
    is_mobile_resolution = False

    is_appium = False
    is_mobile = False
    is_tablet = False

    is_ios = False
    is_ios_tablet = False
    is_ios_mobile = False

    is_android = False
    is_android_tablet = False
    is_android_mobile = False

    is_simulator = False
    is_real_device = False

    browser_name = None

    driver: Union[SeleniumDriver, AppiumDriver, PlaywrightDriver]
    instance: PlaywrightBrowser  # Only for playwright instance
    context: PlaywrightContext  # Only for playwright instance

    def __new__(cls, *args, **kwargs):
        if cls.session.sessions_count() == 0:
            cls = super().__new__(cls)
        else:
            cls = super().__new__(type(f'ShadowDriverWrapper', (cls, ), get_attributes_from_object(cls)))  # noqa

        for name, _ in get_child_elements_with_names(cls, bool).items():
            setattr(cls, name, False)

        return cls

    def __repr__(self):
        cls = self.__class__

        label = 'desktop'
        if cls.is_android:
            label = 'android'
        elif cls.is_ios:
            label = 'ios'

        return f'{cls.__name__}({self.label}={self.driver}) at {hex(id(self))}, platform={label}'

    def __init__(
            self,
            driver: Union[PlaywrightBrowser, AppiumDriver, SeleniumDriver],
            mobile_resolution: Optional[bool] = False,
            *args,
            **kwargs
    ):
        """
        Initializing of driver wrapper based on given driver source

        :param driver: appium or selenium or playwright driver to initialize
        """
        self.driver = driver
        self.session.add_session(self)
        self.label = f'{self.session.all_sessions.index(self) + 1}_driver'
        self.__init_base_class__(*args, **kwargs)
        if mobile_resolution:
            self.is_mobile_resolution = True
            self.is_desktop = False
            self.is_mobile = True

    def quit(self, silent: bool = False, trace_path: str = 'trace.zip'):
        """
        Quit the driver instance

        :param silent: erase log
        :param trace_path: Playwright only: path for the trace
        :return: None
        """
        if not silent:
            self.log('Quit driver instance')

        self._base_cls.quit(self, trace_path)
        self.session.remove_session(self)

    def get_inner_window_size(self) -> dict:
        """
        Get inner size of driver window

        :return: {'height': value, 'width': value}
        """
        return {
            'height': self.execute_script(get_inner_height_js),
            'width': self.execute_script(get_inner_width_js)
        }

    def save_screenshot(
            self,
            file_name: str,
            screenshot_base: Union[bytes, Image] = None,
            convert_type: str = None
    ) -> Image:
        """
        Takes full driver screenshot and saving with given path/filename

        :param file_name: path/filename
        :param screenshot_base: use given image binary instead of taking a new screenshot
        :param convert_type: convert image type before save
        :return: PIL Image object
        """
        self.log(f'Save driver screenshot')

        image_object = screenshot_base
        if type(screenshot_base) is bytes:
            image_object = self.screenshot_image(screenshot_base)

        if convert_type:
            image_object = image_object.convert(convert_type)

        image_object.save(file_name)

        return image_object

    def assert_screenshot(
            self,
            filename: str = '',
            test_name: str = '',
            name_suffix: str = '',
            threshold: Union[int, float] = None,
            delay: Union[int, float] = None,
            remove: Union[Any, List[Any]] = None,
            cut_box: CutBox = None,
            hide: Union[Any, List[Any]] = None,
    ) -> None:
        """
        Assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/negative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param remove: remove elements from screenshot
        :param cut_box: custom coordinates, that will be cut from original image (left, top, right, bottom)
        :param hide: hide elements from page before taking screenshot
        :return: None
        """
        delay = delay or VisualComparison.default_delay
        remove = [remove] if type(remove) is not list and remove else remove

        if hide:
            if not isinstance(hide, list):
                hide = [hide]
            for object_to_hide in hide:
                object_to_hide.hide()

        VisualComparison(self).assert_screenshot(
            filename=filename, test_name=test_name, name_suffix=name_suffix, threshold=threshold, delay=delay,
            scroll=False, remove=remove, fill_background=False, cut_box=cut_box
        )

    def soft_assert_screenshot(
            self,
            filename: str = '',
            test_name: str = '',
            name_suffix: str = '',
            threshold: Union[int, float] = None,
            delay: Union[int, float] = None,
            remove: Union[Any, List[Any]] = None,
            cut_box: CutBox = None,
            hide: Union[Any, List[Any]] = None,
    ) -> Tuple[bool, str]:
        """
        Soft assert given (by name) and taken screenshot equals

        :param filename: full screenshot name. Custom filename will be used if empty string given
        :param test_name: test name for custom filename. Will try to find it automatically if empty string given
        :param name_suffix: filename suffix. Good to use for same element with positive/negative case
        :param threshold: possible threshold
        :param delay: delay before taking screenshot
        :param remove: remove elements from screenshot
        :param cut_box: custom coordinates, that will be cut from original image (left, top, right, bottom)
        :param hide: hide elements from page before taking screenshot
        :return: bool - True: screenshots equal; False: screenshots mismatch;
        """
        try:
            self.assert_screenshot(filename, test_name, name_suffix, threshold, delay, remove, cut_box, hide)
        except AssertionError as exc:
            exc = str(exc)
            self.log(exc, level=LogLevel.ERROR)
            return False, exc

        return True, f'No visual mismatch found for entire screen'

    def __init_base_class__(self, *args, **kwargs) -> None:
        """
        Get driver wrapper class in according to given driver source, and set him as base class

        :return: None
        """
        if isinstance(self.driver, PlaywrightBrowser):
            self.is_playwright = True
            self._base_cls = PlayDriver
        elif isinstance(self.driver, AppiumDriver):
            self.is_appium = True
            self._base_cls = MobileDriver
        elif isinstance(self.driver, SeleniumDriver):
            self.is_selenium = True
            self._base_cls = WebDriver
        else:
            raise DriverWrapperException(f'Cant specify {self.__class__.__name__}')

        self._set_static(self._base_cls)
        self._base_cls.__init__(self, driver=self.driver, *args, **kwargs)

        for name, value in self.__dict__.items():
            setattr(self.__class__, name, value)
