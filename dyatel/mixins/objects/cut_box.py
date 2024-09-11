from __future__ import annotations

import typing
from dataclasses import dataclass

from dyatel.utils.internal_utils import get_dict


@dataclass
class CutBox:
    left: typing.Union[int, float, None] = None
    top: typing.Union[int, float, None] = None
    right: typing.Union[int, float, None] = None
    bottom: typing.Union[int, float, None] = None
    is_percents: bool = False

    def fill_values(self) -> None:
        """
        Fill None values with zero

        :return: None
        """
        for name, value in get_dict(self).items():
            setattr(self, name, value if value else 0)

    def get_box(self, size: tuple) -> tuple:
        """
        Get cut box values

        :param size: initial width, height values of image
        :return: tuple
        """
        width, height = size
        self.fill_values()

        if self.is_percents:
            left = self.left * width / 100 if self.left else self.left
            top = self.top * height / 100 if self.top else self.top
            right = width - self.right * width / 100 if self.right else width
            bottom = height - self.bottom * height / 100 if self.bottom else height
            return left, top, right, bottom

        return self.left, self.top, width-self.right, height-self.bottom

