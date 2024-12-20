from dataclasses import dataclass
from typing import Optional, Any


def take_locator_type(locator: Any):
    """
    Safe take locator type from given object

    :param locator:
    :return:
    """
    return locator.loc_type if type(locator) is Locator else None


@dataclass
class Locator:
    default: Optional[str] = None
    loc_type: Optional[str] = None
    desktop: Optional[str] = None
    mobile: Optional[str] = None
    tablet: Optional[str] = None
    ios: Optional[str] = None
    android: Optional[str] = None
