from dataclasses import dataclass
from typing import Any

from dyatel.exceptions import DriverWrapperException


@dataclass
class Result:
    execution_result: Any
    error: DriverWrapperException = None
