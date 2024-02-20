import typing
from dataclasses import dataclass


@dataclass
class Trace:
    name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    snapshots: typing.Optional[bool] = None
    screenshots: typing.Optional[bool] = None
    sources: typing.Optional[bool] = None
