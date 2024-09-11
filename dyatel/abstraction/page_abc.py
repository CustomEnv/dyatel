from __future__ import annotations

from abc import ABC
from typing import Union

from dyatel.abstraction.mixin_abc import MixinABC
from dyatel.base.element import Element
from dyatel.utils.internal_utils import WAIT_PAGE


class PageABC(MixinABC, ABC):

    def reload_page(self, wait_page_load: bool = True) -> PageABC:
        """
        Reload current page

        :param wait_page_load: wait until anchor will be element loaded
        :return: self
        """
        raise NotImplementedError()

    def open_page(self, url: str = '') -> PageABC:
        """
        Open page with given url or use url from page class f url isn't given

        :param url: url for navigation
        :return: self
        """
        raise NotImplementedError()

    def wait_page_loaded(self, silent: bool = False, timeout: Union[int, float] = WAIT_PAGE) -> PageABC:
        """
        Wait until page loaded

        :param silent: erase log
        :param timeout: page/elements wait timeout
        :return: self
        """
        raise NotImplementedError()

    def is_page_opened(self, with_elements: bool = False, with_url: bool = False) -> bool:
        """
        Check is current page opened or not

        :param with_elements: is page opened with signed elements
        :param with_url: is page opened check with url
        :return: self
        """
        raise NotImplementedError()

    def anchor(self) -> Element:
        """
        Get anchor element of the page

        :return: Element object
        """
        raise NotImplementedError()

    def swipe(
            self,
            start_x: int,
            start_y: int,
            end_x: int,
            end_y: int,
            duration: int = 0,
            sleep: Union[int, float] = 0
    ) -> PageABC:
        """
        Swipe from one point to another point, for an optional duration

        :param start_x: x-coordinate at which to start
        :param start_y: y-coordinate at which to start
        :param end_x: x-coordinate at which to stop
        :param end_y: y-coordinate at which to stop
        :param duration: time to take the swipe, in ms
        :param sleep: delay after swipe
        :return: self
        """
        raise NotImplementedError()

    def swipe_down(self) -> PageABC:
        """
        Swipe page down

        :return: self
        """
        raise NotImplementedError()

    def swipe_up(self) -> PageABC:
        """
        Swipe page up

        :return: self
        """
        raise NotImplementedError()
