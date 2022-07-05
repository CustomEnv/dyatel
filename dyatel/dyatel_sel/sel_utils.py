from selenium.webdriver.common.by import By

from dyatel.internal_utils import all_tags


def get_locator_type(locator: str):
    """
    Get selenium completable locator type by given locator spell

    :param locator: regular locator
    :return:
      By.TAG_NAME if locator contain tag name
      By.XPATH if locator contain slashes and brackets
      By.CSS_SELECTOR if locator contain brackets and no slash
      By.CSS_SELECTOR if locator contain dot and no brackets
      By.ID if there is no any match
    """
    brackets = '[' in locator and ']' in locator
    is_only_tags = True

    if locator in all_tags:
        return By.TAG_NAME
    elif '/' in locator:
        return By.XPATH
    elif '/' not in locator and brackets:
        return By.CSS_SELECTOR
    elif '.' in locator and not brackets:
        return By.CSS_SELECTOR

    for tag in locator.split(' '):
        is_only_tags = is_only_tags and tag in all_tags

    if is_only_tags:
        return By.TAG_NAME

    return By.ID


def get_legacy_selector(locator, locator_type):
    """
    Workaround for using same locators for selenium and appium objects.
    More info here https://github.com/appium/python-client/pull/724

    :param locator: regular locator
    :param locator_type: updated locator type from get_locator_type
    :return: selenium like locator and locator_type
    """
    if locator_type == By.ID:
        locator_type = By.CSS_SELECTOR
        locator = f'[id="{locator}"]'
    elif locator_type == By.TAG_NAME:
        locator_type = By.CSS_SELECTOR
    elif locator_type == By.CLASS_NAME:
        locator_type = By.CSS_SELECTOR
        locator = f".{locator}"
    elif locator_type == By.NAME:
        locator_type = By.CSS_SELECTOR
        locator = f'[name="{locator}"]'
    return locator, locator_type
