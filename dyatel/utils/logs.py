from __future__ import annotations

import logging
import sys
from functools import lru_cache
from os.path import basename
from typing import Any

from dyatel.utils.internal_utils import get_frame, is_driver_wrapper


logger = logging.getLogger('dyatel')


class LogLevel:
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'


def dyatel_logs_settings(level: str = LogLevel.INFO) -> None:
    """
    Sets dyatel log format(unchangeable) and log level (can be changed)

    :param level: log level to be captured. Example: DEBUG - all, CRITICAL - only highest level priority level
    :return: None
    """
    handler = logging.StreamHandler(sys.stdout)
    level = getattr(logging, level.upper())
    logger.setLevel(level)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d][%(levelname).1s]%(message)s',
        datefmt="%h %d][%H:%M:%S"
    ))
    logger.addHandler(handler)


def autolog(message: Any, level: str = LogLevel.INFO) -> None:
    """
    Log message in format:
      ~ [time][level][module][function:line] <message>
      ~ [Aug 14][16:04:22.767][I][play_element.py][is_displayed:328] Check visibility of "Mouse page"

    :param message: info message
    :param level: log level
    :return: None
    """
    _send_log_message(str(message), level)


class Logging:

    def log(self: Any, message: str, level: str = LogLevel.INFO) -> None:
        """
        Log message in format:
          ~ [time][level][driver_index][module][function:line] <message>
          ~ [Aug 14][16:04:22.767][I][2_driver][play_element.py][is_displayed:328] Check visibility of "Mouse page"

        :param message: info message
        :param level: log level
        :return: None
        """
        if is_driver_wrapper(self):
            label = self.label
        else:
            label = self.driver_wrapper.label

        _send_log_message(f'[{label}]{self._get_code_info()} {message}', level)
        return None

    def _get_code_info(self) -> str:
        """
        Get executed code info: filename/function name/line

        :return: log message
        """
        code = get_frame(3).f_code
        return f'[{basename(code.co_filename)}][{code.co_name}:{code.co_firstlineno}]'


def _send_log_message(log_message: str, level: str) -> None:
    """
    Send log message

    :param level: log level
    :param log_message: custom message
    :return: None
    """
    logger.log(_get_log_level(level), log_message)


@lru_cache(maxsize=None)
def _get_log_level(level: str) -> int:
    """
    Get log level from string. Moved to a different function for using @lru_cache

    :param level: string level ~ INFO, DEBUG etc.
    :return: log level in int format
    """
    return getattr(logging, level.upper())
