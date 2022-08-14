from __future__ import annotations

import logging
from inspect import currentframe
from os.path import basename

from dyatel.js_scripts import add_driver_index_comment_js

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s.%(msecs)03d][%(levelname).1s]%(message)s',
    datefmt="%h %d][%H:%M:%S"
)


def get_log_message(message) -> str:
    code = currentframe().f_back.f_back.f_code
    return f'[{basename(code.co_filename)}][{code.co_name}:{code.co_firstlineno}] {message}'


def send_log_message(level, log_message) -> None:
    logging.log(getattr(logging, level.upper()), log_message)


def autolog(message, level='info') -> None:
    """
    Log message in format:
      ~ [time][level][module][function:line] <message>
      ~ [Aug 14][16:04:22.767][I][play_element.py][is_displayed:328] Check visibility of "Mouse page"

    :param message: info message
    :param level: log level
    :return: None
    """
    send_log_message(message, level)


class LogMixin:
    driver = None
    driver_wrapper = None

    def log(self, message, level='info') -> LogMixin:
        """
        Log message in format:
          ~ [time][level][driver_index][module][function:line] <message>
          ~ [Aug 14][16:04:22.767][I][2_driver][play_element.py][is_displayed:328] Check visibility of "Mouse page"

        :param message: info message
        :param level: log level
        :return: None
        """
        driver_log = ''

        if len(self.driver_wrapper.all_drivers) > 1:
            driver_index = str(self.driver_wrapper.all_drivers.index(self.driver) + 1)
            driver_log = f'[{driver_index}_driver]'

            if not hasattr(self.driver, 'driver_index'):
                self.driver.driver_index = driver_index

            if self.driver_wrapper.selenium:
                self.driver_wrapper.execute_script(add_driver_index_comment_js, driver_index)

        send_log_message(level, f'{driver_log}{get_log_message(message)}')
        return self
