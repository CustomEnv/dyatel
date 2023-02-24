from __future__ import annotations

from typing import List

from dyatel.dyatel_play.play_element import PlayElement
from dyatel.mixins.internal_utils import get_child_elements, initialize_objects, get_child_elements_with_names
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.log_mixin import LogMixin


class PlayPage(DriverMixin, LogMixin):

    def __init__(self):
        self._element = None
        self.url = getattr(self, 'url', '')

        initialize_objects(self, get_child_elements_with_names(self, PlayElement))
        self.page_elements: List[PlayElement] = get_child_elements(self, PlayElement)
