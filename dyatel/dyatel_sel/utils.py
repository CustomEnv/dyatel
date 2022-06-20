from selenium.webdriver.common.by import By

tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link']


def get_locator_type(locator):
    brackets = '[' in locator and ']' in locator

    if locator in tags:
        return By.TAG_NAME
    elif '/' in locator:
        return By.XPATH
    elif '/' not in locator and brackets:
        return By.CSS_SELECTOR
    elif '.' in locator and not brackets:
        return By.CSS_SELECTOR
    else:
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
