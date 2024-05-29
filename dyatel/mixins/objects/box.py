from __future__ import annotations

import typing
from dataclasses import dataclass

from dyatel.utils.internal_utils import get_dict


@dataclass
class Box:
    x: typing.Union[int, float, None] = None
    y: typing.Union[int, float, None] = None
    width: typing.Union[int, float, None] = None
    height: typing.Union[int, float, None] = None

    def fill_values(self) -> Box:
        """
        Fill None values with zero

        :return: self
        """
        for name, value in get_dict(self).items():
            setattr(self, name, value if value else 0)

        return self
