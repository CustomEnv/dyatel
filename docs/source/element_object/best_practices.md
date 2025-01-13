# Element Best Practices

When using a `Element` class in your test automation framework, following best practices can significantly enhance the
readability, maintainability, and effectiveness of your test code. Here are key best practices to consider when writing
`Element` objects:

<br>

## 1. Use Element as attributes

The primary use case for `Element` is as a class attribute of `Group` or `Page` classes. 
This allows you to organize and manage multiple UI elements within a container or page.

### Code example

```python
from mops.base.page import Page
from mops.base.element import Element


class IndexPage(Page):

    def __init__(self):
        super().__init__()

    login_button = Element('button.login', name='login button')
    signup_button = Element('button.signup', name='signup button')
```

---

<br>

## 2. Extend the Element

In some cases, you might want to create a custom UI element that extends or change the functionality of `Element`. 
This is particularly useful when you need to add specific behaviors or properties.

### Code example

```python
from mops.base.page import Page
from mops.base.element import Element


class IndexButton(Element):

    def __init__(self, locator: str, name: str = ''):
        name = name or locator
        super().__init__(f'button.{locator}', name=f'{name} button')

    def click(self):  # noqa
        # Add custom behavior here
        super().click()


# Using previous PO with IndexButton
class IndexPage(Page):

    def __init__(self):
        super().__init__()

    login_button = IndexButton('login')
    signup_button = IndexButton('signup')
```

In this example, `IndexButton` inherits from `Element` and mutates the given `locator`/`name` args.
This allows you to create buttons with different or extended functionality while still benefiting from the base `Element` functionality.
