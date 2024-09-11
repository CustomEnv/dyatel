from dataclasses import dataclass
from typing import Optional, Any

ios_mobile_small_bottom_bar_locator = '//*[@name="CapsuleViewController"]/XCUIElementTypeOther[1]'
ios_mobile_large_bottom_bar_locator = '//*[@name="CapsuleViewController"]/XCUIElementTypeOther[3]'
ios_tablet_top_bar_locator = '//XCUIElementTypeOther[@name="UnifiedBar?isStandaloneBar=true"]/XCUIElementTypeOther[1]'
ios_mobile_top_bar_locator = '//*[contains(@name, "SafariWindow")]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther'  # noqa
ios_keyboard_hide_button = "//XCUIElementTypeButton[@name='Done']"


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
