# Group Best Practices

When using a `Group` class in your test automation framework, following best practices can significantly enhance the
readability, maintainability, and effectiveness of your test code. Here are key best practices to consider when writing
`Group` objects:

<br>

## 1. Keep Group classes concise

<br>

A well-designed `Group` object should be concise and focused on a specific section or component. Avoid making the `Group class overly lengthy, as this can hinder readability and make maintenance more challenging.

<br>

### Recommendations
- **Limit Lines of Code**: Strive to keep the `Group` class manageable by limiting the number of lines. A concise `Group`` class is easier to read and understand.
- **Separate Concerns**: If a `Group` class becomes too large, consider breaking it down into smaller, more focused classes or components if the framework supports it.

---

## 2. Group Element attributes

<br>

When a `Group` contains many elements (more than 8-10), it is advisable to group them logically. This helps in organizing the code and improves readability.

<br>

### Recommendations
- **Logical Grouping**: Group elements based on their functionality. For example, group footer controls, header controls, or form fields together.
- **Use Descriptive Names**: Use clear and descriptive names for the groups and individual elements to enhance clarity.

<br>

### Good practice

Here’s how you can organize a `Group` object with a large number of elements by grouping them logically:

```python
from mops.base.group import Group
from mops.base.element import Element


class SeeMoreSection(Group):

    def __init__(self):
        super().__init__(...)

    # Footer Controls
    see_more_footer_logout_button = Element('#footer-logout', name='Footer Logout Button')
    see_more_footer_help_link = Element('#footer-help', name='Footer Help Link')
    see_more_footer_contact_us = Element('#footer-contact', name='Footer Contact Us')

    # Header Controls
    see_more_header_notifications_icon = Element('#header-notifications', name='Header Notifications Icon')
    see_more_header_user_profile = Element('#header-profile', name='Header User Profile')
    see_more_header_search_box = Element('#header-search', name='Header Search Box')

    # Main Content Controls
    see_more_main_content_title = Element('#main-title', name='Main Content Title')
    see_more_main_content_body = Element('#main-body', name='Main Content Body')
```

---

## 3. Reduce `parent` arg abusing

<br>

```{note}
This section describes a refactoring approach to reduce excessive usage of the `parent` argument within the `Group` class
For detailed information, how `parent` arg work within `Group` class please refer to {doc}`Group Key Features <./key_features>`
```

<br>

### The Problem

The `parent` argument allows you to specify a parent context from which the element's location on the page will be 
determined. However, it should be used sparingly and only as an exception. And here is why...

The provided code demonstrates two ways to define elements within a `SeeMoreSection` class inheriting from `Group`. 
The "Bad example" relies heavily on the `parent` argument for elements within the "Footer Controls" section. 
This can lead to:

* **Reduced Readability:** The code becomes cluttered with repeated usage of `parent`.
* **Maintainability Issues:** Changes to the parent element might require modifying multiple child elements.
* **Deviation from the PCOM standard:** The Page Component Object Model standard is no longer being met.

<br>

### The Solution

The "Good example" showcases a better approach by defining a separate class named `SeeMoreFooter` that inherits from 
`Group`. This class encapsulates the footer elements, improving code organization and maintainability.

<br>

### Benefits

By following this approach, you achieve:

* **Improved Code Readability:** The code becomes more structured and easier to understand.
* **Enhanced Maintainability:** Changes to parent elements or child elements are isolated within their respective classes.
* **Potential Code Reuse:** The dedicated class can be reused in other parts of your codebase if applicable.

<br>

### Bad practice

```python
from mops.base.group import Group
from mops.base.element import Element


class SeeMoreSection(Group):

    def __init__(self):
        super().__init__(...)

    # Footer Controls
    see_more_footer_main_control = Element('#footer-main', name='footer main control')
    see_more_footer_logout_button = Element('#footer-logout', name='Footer Logout Button',
                                            parent=see_more_footer_main_control)
    see_more_footer_help_link = Element('#footer-help', name='Footer Help Link',
                                        parent=see_more_footer_main_control)
    see_more_footer_contact_us = Element('#footer-contact', name='Footer Contact Us',
                                         parent=see_more_footer_main_control)

    # Header Controls
    see_more_header_notifications_icon = Element('#header-notifications', name='Header Notifications Icon')
    see_more_header_user_profile = Element('#header-profile', name='Header User Profile')
    see_more_header_search_box = Element('#header-search', name='Header Search Box')

    # Main Content Controls
    see_more_main_content_title = Element('#main-title', name='Main Content Title')
    see_more_main_content_body = Element('#main-body', name='Main Content Body')
```

<br>

### Good practice

```python
from mops.base.group import Group
from mops.base.element import Element


class SeeMoreFooter(Group):

    def __init__(self):
        super().__init__('#footer-main', name='footer main control')

    see_more_footer_logout_button = Element('#footer-logout', name='Footer Logout Button')
    see_more_footer_help_link = Element('#footer-help', name='Footer Help Link')
    see_more_footer_contact_us = Element('#footer-contact', name='Footer Contact Us')


class SeeMoreSection(Group):

    def __init__(self):
        super().__init__(...)

    footer = SeeMoreFooter()

    # Header Controls
    see_more_header_notifications_icon = Element('#header-notifications', name='Header Notifications Icon')
    see_more_header_user_profile = Element('#header-profile', name='Header User Profile')
    see_more_header_search_box = Element('#header-search', name='Header Search Box')

    # Main Content Controls
    see_more_main_content_title = Element('#main-title', name='Main Content Title')
    see_more_main_content_body = Element('#main-body', name='Main Content Body')
```
