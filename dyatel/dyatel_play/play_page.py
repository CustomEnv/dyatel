from __future__ import annotations

from typing import List

from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_utils import get_selenium_completable_locator
from dyatel.mixins.internal_utils import get_child_elements, initialize_objects_with_args, get_child_elements_with_names
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.log_mixin import LogMixin


class PlayPage(DriverMixin, LogMixin):

    def __init__(self, locator: str, locator_type: str, name: str):
        """
        Initializing of web page with playwright driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self._element = None

        self.locator = get_selenium_completable_locator(locator)
        self.name = name if name else self.locator
        self.locator_type = f'{locator_type} - locator_type does not supported for playwright'

        self.url = getattr(self, 'url', '')
        initialize_objects_with_args(self, get_child_elements_with_names(self, PlayElement))
        self.page_elements: List[PlayElement] = get_child_elements(self, PlayElement)
