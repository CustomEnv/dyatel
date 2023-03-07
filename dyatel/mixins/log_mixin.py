from __future__ import annotations

import logging
import sys
from os.path import basename
from typing import Any

from selenium.common import WebDriverException as SeleniumWebDriverException

from dyatel.js_scripts import add_driver_index_comment_js, find_comments_js
from dyatel.mixins.core_mixin import get_frame, driver_with_index


def dyatel_logs_settings():
    logging.getLogger('WDM').setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s.%(msecs)03d][%(levelname).1s]%(message)s',
        datefmt="%h %d][%H:%M:%S",
        stream=sys.stdout
    )


def get_log_message(message: str) -> str:
    """
    Get log message with code

    :param message: custom message
    :return: log message
    """
    code = get_frame(3).f_code
    return f'[{basename(code.co_filename)}][{code.co_name}:{code.co_firstlineno}] {message}'


def send_log_message(log_message: str, level: str, ) -> None:
    """
    Send log message

    :param level: log level
    :param log_message: custom message
    :return: None
    """
    try:
        # workaround for https://github.com/pytest-dev/pytest/issues/5502
        logging.log(getattr(logging, level.upper()), log_message)
    except ValueError:
        pass


def autolog(message: Any, level: str = 'info') -> Any:
    """
    Log message in format:
      ~ [time][level][module][function:line] <message>
      ~ [Aug 14][16:04:22.767][I][play_element.py][is_displayed:328] Check visibility of "Mouse page"

    :param message: info message
    :param level: log level
    :return: message
    """
    send_log_message(str(message), level)
    return message


class LogMixin:

    def log(self, message: str, level: str = 'info') -> None:
        """
        Log message in format:
          ~ [time][level][driver_index][module][function:line] <message>
          ~ [Aug 14][16:04:22.767][I][2_driver][play_element.py][is_displayed:328] Check visibility of "Mouse page"

        :param message: info message
        :param level: log level
        :return: None
        """
        driver = getattr(self, 'driver')
        driver_wrapper = getattr(self, 'driver_wrapper')
        driver_log, index = '', driver_with_index(driver_wrapper, driver)

        if index:
            driver_log = f'[{index}]'

            try:
                if driver_wrapper.selenium:
                    if '_driver' not in str(driver_wrapper.execute_script(find_comments_js)):
                        driver_wrapper.execute_script(add_driver_index_comment_js, index)
            except SeleniumWebDriverException:
                pass

        send_log_message(f'{driver_log}{get_log_message(message)}', level)
        return None
