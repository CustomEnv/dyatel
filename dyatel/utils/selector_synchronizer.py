from __future__ import annotations

from typing import Any, Union

from selenium.webdriver.common.by import By

from dyatel.exceptions import InvalidSelectorException
from dyatel.mixins.objects.locator import Locator
from dyatel.utils.internal_utils import get_child_elements, all_tags


selenium_locator_types = get_child_elements(By, str)


def get_platform_locator(obj: Any):
    """
    Get locator for current platform from object

    :param obj: Page/Group/Element
    :return: current platform locator
    """
    locator: Union[Locator, str] = obj.locator

    if type(locator) is str or not obj.driver_wrapper:
        return locator

    mobile_fallback_locator = locator.mobile or locator.default

    if obj.driver_wrapper.is_tablet:
        locator = locator.tablet or locator.default
    elif obj.driver_wrapper.is_android:
        locator = locator.android or mobile_fallback_locator
    elif obj.driver_wrapper.is_ios:
        locator = locator.ios or mobile_fallback_locator
    elif obj.driver_wrapper.is_mobile or obj.driver_wrapper.is_appium:
        locator = mobile_fallback_locator
    elif obj.driver_wrapper.is_desktop:
        locator = locator.desktop or locator.default

    return locator


def get_selenium_locator_type(locator: str):
    """
    Get selenium completable locator type by given locator spell

    :param locator: regular locator
    :return:
      By.ID if locator contain ":id" - com.android locator
      By.TAG_NAME if locator contain tag name
      By.XPATH if locator contain slashes and brackets
      By.CSS_SELECTOR if locator contain brackets and no slash
      By.CSS_SELECTOR if locator contain dot and no brackets
      By.ID if there is no any match
    """
    if locator in selenium_locator_types:
        raise InvalidSelectorException(
            f'An locator_type given instead of locator. Ensure your locator is not one of {selenium_locator_types}'
        )

    brackets = '[' in locator and ']' in locator
    is_only_tags = True

    if locator in all_tags:
        return By.TAG_NAME
    elif ':id' in locator:  # Mobile com.android selector
        return By.ID
    elif '/' in locator:
        return By.XPATH
    elif '/' not in locator and brackets:
        return By.CSS_SELECTOR
    elif '.' in locator and not brackets:
        return By.CSS_SELECTOR
    elif '#' in locator:
        return By.CSS_SELECTOR

    for tag in locator.split(' '):
        is_only_tags = is_only_tags and tag in all_tags

    if is_only_tags:
        return By.TAG_NAME

    return By.ID


def get_appium_selector(locator: str, locator_type: str):
    """
    Workaround for using same locators for selenium and appium objects.
    More info here https://github.com/appium/python-client/pull/724

    :param locator: regular locator
    :param locator_type: updated locator type from get_locator_type
    :return: selenium like locator and locator_type
    """
    if locator_type == By.ID:
        locator = f'[id="{locator}"]'
        locator_type = By.CSS_SELECTOR
    elif locator_type == By.TAG_NAME:
        locator_type = By.CSS_SELECTOR
    elif locator_type == By.CLASS_NAME:
        locator = f".{locator}"
        locator_type = By.CSS_SELECTOR
    elif locator_type == By.NAME:
        locator = f'[name="{locator}"]'
        locator_type = By.CSS_SELECTOR
    return locator, locator_type


def get_playwright_locator(locator: str):
    """
    Get playwright locator from selenium based

    :param locator: locator in selenium format ~ '//div[@class="some-class"]'
    :return: locator in playwright format ~ 'xpath=//div[@class="some-class"]'
    """
    brackets = '[' in locator and ']' in locator

    if 'xpath=' in locator or 'id=' in locator:
        return locator

    if locator in all_tags:
        return locator
    elif '/' in locator:
        return f'xpath={locator}'
    elif '/' not in locator and brackets:
        return locator
    elif '.' in locator and not brackets:
        return locator
    elif '#' in locator:
        return locator
    else:
        return f'id={locator}'
