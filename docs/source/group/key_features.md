# Group Key Features

```{note}
Here you will find information on complex or ambiguous functionality. 
For a comprehensive list of all available methods, 
please refer to the {doc}`Group Interface <./interface>` documentation.
```

The `Group` class extends the `Element` class to provide a mechanism for grouping related elements together and managing
their context within a web page. This grouping facilitates the creation of more organized and reusable 
Page Component Object Models (PCOM).

<br>

## 1. Context Management

The primary distinction between `Group` and `Element` is the ability to change the context from which element locators
are resolved. By default, elements are located within the entire browser window. However, when an element is defined
as an attribute within a `Group` class, its locator is searched within the context of the `Group`'s locator.

The `Group` class offers flexibility in defining parent-child relationships. 
The `parent` arg of `Element` can be set to `False` to opt out of automatic assignment or to any other `Element` 
to create custom hierarchies. For more details, how `Element` object works refer to {doc}`Element documentation <../element/index>`

<br>

### Implementation details

The `Group` class automatically sets the `parent` argument for all of its element-based attributes during initialization.
This `parent` value is used to determine the context within which the element's locator should be searched.

<br>

### Code example

```python
from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.driver_wrapper import DriverWrapper

class Section(Group):
    def __init__(self):
        super().__init__('.section', name='section')

    section_button = Element('.button', name='section button')
    section_footer = Element('.footer', name='section button', parent=False)
    section_footer_link = Element('.link', name='section button', parent=section_footer)
    
    data = 'section data'
    

# pytest usage    
def test_section_verification(driver_wrapper: DriverWrapper):
    section = Section()
    assert section.section_button.is_displayed()
    assert section.section_footer_link.text == 'www.example.com'
```

<br>

**Code Explanation - Section initialization:**

* Automatically sets the `parent` argument for the `section_button` attribute to the `Section` instance.
* Does not set the `parent` argument for the `section_footer` attribute because its own `parent` argument is `False`.
* Does not set the `parent` argument for the `section_footer_link` attribute because its own `parent` argument already is `section_footer`.
* Does not set the `parent` argument for the `data` attribute because it is not an instance of the `Element` object.

<br>

**Code Explanation - Behavior when methods are called:**

* When the `is_displayed()` method of `section_button` is called:
    * The driver will initially search for the `Section` locator.
    * Then, it will proceed to locate the `section_button` element within the `Section` context.
* When the `text` property of `section_footer_link` is called:
    * The driver will initially search for the `section_footer` locator.
    * Then, it will proceed to locate the `section_footer_link` element within the `section_footer` context.
