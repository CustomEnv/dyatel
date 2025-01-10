from dataclasses import dataclass
from typing import Any

from mops.exceptions import DriverWrapperException


@dataclass
class Result:
    execution_result: Any
    log: str = None
    exc: DriverWrapperException = None
