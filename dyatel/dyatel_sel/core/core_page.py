from __future__ import annotations

from typing import List

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.mixins.core_mixin import get_child_elements, initialize_objects, get_child_elements_with_names
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.mixins.logging import Logging


class CorePage(DriverMixin, Logging):
    pass
