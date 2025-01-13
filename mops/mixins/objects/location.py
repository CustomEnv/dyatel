import typing
from dataclasses import dataclass


@dataclass
class Location:
    x: typing.Union[int, float, None] = None
    y: typing.Union[int, float, None] = None
