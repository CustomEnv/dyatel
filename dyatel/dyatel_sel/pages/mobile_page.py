from __future__ import annotations

import time
from abc import ABC
from typing import Union

from dyatel.abstraction.page_abc import PageABC
from dyatel.dyatel_sel.core.core_page import CorePage


class MobilePage(CorePage, PageABC, ABC):

    def swipe(
            self,
            start_x: int,
            start_y: int,
            end_x: int,
            end_y: int,
            duration: int = 0,
            sleep: Union[int, float] = 0
    ) -> MobilePage:
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
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(sleep)
        return self

    def swipe_down(self) -> MobilePage:
        """
        Swipe page down

        :return: self
        """
        self.swipe(0, 500, 0, 100, sleep=0.1)
        return self

    def swipe_up(self) -> MobilePage:
        """
        Swipe page up

        :return: self
        """
        self.swipe(0, 100, 0, 500, sleep=0.1)
        return self
