from __future__ import annotations

from typing import List

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.mixins.core_mixin import get_child_elements, initialize_objects, get_child_elements_with_names
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.log_mixin import LogMixin


class CorePage(DriverMixin, LogMixin):

    def __init__(self):
        self._element = None
        self.url = getattr(self, 'url', '')

        initialize_objects(self, get_child_elements_with_names(self, CoreElement))
        self.page_elements: List[CoreElement] = get_child_elements(self, CoreElement)
