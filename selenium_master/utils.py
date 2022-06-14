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
