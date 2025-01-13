import typing
from dataclasses import dataclass


@dataclass
class Size:
    width: typing.Union[int, float, None] = None
    height: typing.Union[int, float, None] = None
