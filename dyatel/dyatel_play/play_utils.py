tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'head', 'body', 'input', 'section', 'button', 'a', 'link']


def get_selenium_completable_locator(locator):
    brackets = '[' in locator and ']' in locator

    if 'xpath=' in locator or 'id=' in locator:
        return locator

    if locator in tags:
        return locator
    elif '/' in locator:
        return f'xpath={locator}'
    elif '/' not in locator and brackets:
        return locator
    elif '.' in locator and not brackets:
        return locator
    else:
        return f'id={locator}'
