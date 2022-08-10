from __future__ import annotations

import time
from typing import Union

from dyatel.dyatel_sel.core.core_page import CorePage


class MobilePage(CorePage):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of mobile page with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        super().__init__(locator=locator, locator_type=locator_type, name=name)

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int,
              duration: int = 0, sleep: Union[int, float] = 0) -> MobilePage:
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

    def swipe_down(self):
        """
        Swipe page down

        :return:
        """
        self.swipe(0, 500, 0, 100, sleep=0.1)

    def swipe_up(self):
        """
        Swipe page up

        :return:
        """
        self.swipe(0, 100, 0, 500, sleep=0.1)
