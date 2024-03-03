import typing
from dataclasses import dataclass


@dataclass
class Box:
    x: typing.Union[int, float, None] = None
    y: typing.Union[int, float, None] = None
    width: typing.Union[int, float, None] = None
    height: typing.Union[int, float, None] = None
