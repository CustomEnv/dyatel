# Page Key Features

```{note}
Only a few methods are described here, due to their complexity. For a comprehensive list of all available 
methods, please refer to the {doc}`Page Interface <./interface>` documentation.
```

The `Page` class is equipped with methods to manage and verify the state of web pages during automated testing. 
Two complex methods, `wait_page_loaded` and `is_page_opened`, provide functionality to handle page loading and 
validation effectively. Below are the details for each method.

## Key Methods

<br>

### 1. Method `wait_page_loaded`

The `wait_page_loaded` method is designed to wait until the page and its elements are fully loaded. 
This is crucial for ensuring that your interactions with the page occur only after all necessary elements are available.

#### Parameters

- **`silent`** (`bool`): When set to `True`, the method suppresses logging messages. If `False`, the method logs a message indicating that it is waiting for the page to load.
- **`timeout`** (`Union[int, float]`): Specifies the maximum time (in seconds) to wait for the page and its elements to load. This parameter can be set to a custom value or use the default `WAIT_PAGE` value.

#### Functionality

1. **Anchor Element Wait**:
   - The method waits for the `anchor` element (a key element indicating that the page has loaded) to be visible using the specified timeout.

2. **Element Waits**:
   - The method iterates through `self.page_elements` and waits for each element according to its `wait` attribute:
     - If `wait` is `False`, it waits until the element is hidden.
     - If `wait` is `True`, it waits until the element is visible.

#### Example Usage

```python
from dyatel.base.page import Page
from dyatel.base.element import Element

class LoginPage(Page):
    
    def __init__(self):
        super().__init__('.login.page', name='Login page')
    
    loader = Element('.loader', name='loader', wait=False)
    form = Element('.login.form', name='login form', wait=True)


# pytest usage
def test_wait_page_load(driver_wrapper):
    LoginPage().wait_page_loaded()
```
**Code Explanation**

The `page.wait_page_loaded()` line will wait for:
1. `anchor` internal Element visibility of `LoginPage` which is ".login.page"
2. `loader` Element invisibility of `LoginPage`
3. `form` Element visibility of `LoginPage`

<br>

---

### 2. Method `is_page_opened`

The `is_page_opened` method is designed to determine if the current page is opened and ready for interaction. 
This method checks several conditions to confirm that the page is in the expected state.

#### Parameters

- **`with_elements`** (`bool`): If set to `True`, the method will verify that the page elements defined in `self.page_elements` are visible and displayed. This ensures that key elements on the page are present and accessible.
- **`with_url`** (`bool`): If set to `True`, the method will also check that the current URL of the page matches the expected URL (`self.url`). This helps ensure that the browser is on the correct page.

#### Functionality

1. **Element Visibility Check**:
   - The method iterates through `self.page_elements` to check if each `Element(..., wait=True)` is visible on the page, if the `with_elements` parameter is `True`.

2. **Anchor Visibility Check**:
   - It checks if the `anchor` internal `Element` (presumably a key element indicating that the page has loaded) is displayed.

3. **URL Check**:
   - If `with_url` is `True`, it verifies that the current URL of the page matches the expected URL stored in `self.url`.

#### Example Usage

```python
from dyatel.base.page import Page
from dyatel.base.element import Element

class LoginPage(Page):
    
    def __init__(self):
        super().__init__('.login.page', name='Login page')
    
    loader = Element('.loader', name='loader', wait=False)
    form = Element('.login.form', name='login form', wait=True)

    
# pytest usage
def test_wait_page_load(driver_wrapper):
    assert LoginPage().is_page_opened(with_elements=True, with_url=False)
```
**Code Explanation**

The `is_page_opened(...)` method will return status of:
1. `anchor` internal Element visibility of `LoginPage` which is ".login.page"
2. `form` Element visibility of `LoginPage`
3. `url` equality will be skipped according to `with_url=False`
