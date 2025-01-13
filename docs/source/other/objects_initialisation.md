# Objects Initialization

```{hint} 
`PGE`: abbreviation of classes that inherits from `Page`, `Group`, or `Element` which used as a 
Page Object Model (POM) or Page Component Object Model (PCOM).
```

## Overview

The `PGE` class is designed to streamline the interaction with web elements by automatically initializing all class 
attributes that are instances of the `Element` class. This initialization occurs recursively during the `PGE` class 
instantiation, ensuring that all elements are ready for interaction as soon as the `PGE` object is created.

<br>

### `PGE` Initialization

When an instance of the `PGE` class is created, it automatically initializes all attributes within 
the class that are instances of the `Element` object **if** there are at least one active `DriverWrapper`. 
This process is performed recursively, meaning that if an `Group/Element` object  contains other `Group/Element`
objects as attributes, those too will be initialized.


#### How It Works

1. **Class Scanning**: During the initialization of a `PGE` object, the class is scanned for all attributes that are instances of the `Element` class.
2. **Recursive Initialization**: Each `Element` attribute is initialized recursively, ensuring that nested elements are also prepared for interaction.
3. **Ready-to-Use Elements**: Once the `PGE` object is fully initialized, all `Element` instances are ready to be used in your test scripts without any additional setup.

<br>

### Handling `driver_wrapper` arg  within `PGE`

1. The `driver_wrapper` is an essential component when working with multiple drivers in your automation framework. 
2. The `PGE` class and its attributes will use the provided `driver_wrapper` to interact with the appropriate web driver. 
3. The `driver_wrapper` argument can accept either a `DriverWrapper` object or any object that contains a `driver_wrapper` attribute.
4. The provided `driver_wrapper` object will be automatically integrated into the all `PGE` attributes.

#### Usage of `driver_wrapper` arg

- **Single Driver Scenario**: If you're using a single driver for your automation, the `driver_wrapper` argument is typically set once automatically at the beginning and used throughout the entire session.
- **Multiple Drivers Scenario**: When your test setup requires interacting with multiple drivers, the `driver_wrapper` argument allows you to specify which driver to use for each `PGE` object. This ensures that each page and its elements operate within the correct context.

<br>

#### Code example

```python
from typing import Union, Any

from mops.base.page import Page
from mops.base.group import Group
from mops.base.element import Element
from mops.base.driver_wrapper import DriverWrapper


# POM
class LoginPage(Page):
    def __init__(self, driver_wrapper: Union[Any, DriverWrapper]):
        super().__init__(locator="//form[@id='login']", name="Login Page", driver_wrapper=driver_wrapper)

    username_field = Element('.username_field', name='username field')
    password_field = Element('.password_field', name='password field')
    login_button = Element('.login_button', name='login button')

# PCOM


class LoginSection(Group):
    def __init__(self, driver_wrapper: Union[Any, DriverWrapper]):
        super().__init__(locator="//form[@id='section']", name="Login section", driver_wrapper=driver_wrapper)

    username_field = Element('.username_field', name='username field')
    password_field = Element('.password_field', name='password field')
    login_button = Element('.login_button', name='login button')

# The framework allow to use Element as base class, but it's better to not use it as POM/PCOM


# But it's possible to use it as a wrapper for Element for extend/change some logic
class Tooltip(Element):
    tooltip_container = Element('.tooltip', name='base tooltip')

    @property
    def text(self):
        return self.tooltip_container.text
```