# Page Best Practices

When using a Page class in your test automation framework, following best practices can significantly enhance the
readability, maintainability, and effectiveness of your test code. Here are key best practices to consider when writing
Page Objects:

<br>

## 1. Keep Page Classes Concise

A well-designed Page Object should be concise and focused on a specific page or component. Avoid making the page class overly lengthy, as this can hinder readability and make maintenance more challenging.

### Recommendations
- **Limit Lines of Code**: Strive to keep the page class manageable by limiting the number of lines. A concise page class is easier to read and understand.
- **Separate Concerns**: If a page class becomes too large, consider breaking it down into smaller, more focused classes or components if the framework supports it.

<br>

---

## 2. Group Element Attributes

When a page contains many elements (more than 8-10), it is advisable to group them logically. This helps in organizing the code and improves readability.

### Recommendations
- **Logical Grouping**: Group elements based on their functionality or section of the page. For example, group footer controls, header controls, or form fields together.
- **Use Descriptive Names**: Use clear and descriptive names for the groups and individual elements to enhance clarity.

### Example

Here’s how you can organize a Page Object with a large number of elements by grouping them logically:

```python
from mops.base.page import Page
from mops.base.element import Element


class DashboardPage(Page):

    def __init__(self):
        super().__init__(...)

    # Footer Controls
    footer_logout_button = Element('#footer-logout', name='Footer Logout Button')
    footer_help_link = Element('#footer-help', name='Footer Help Link')
    footer_contact_us = Element('#footer-contact', name='Footer Contact Us')

    # Header Controls
    header_notifications_icon = Element('#header-notifications', name='Header Notifications Icon')
    header_user_profile = Element('#header-profile', name='Header User Profile')
    header_search_box = Element('#header-search', name='Header Search Box')

    # Main Content Controls
    main_content_title = Element('#main-title', name='Main Content Title')
    main_content_body = Element('#main-body', name='Main Content Body')

    def navigate_to_settings(self):
        """
        Navigate to the settings page.
        """
        self.header_user_profile.click()
        # Additional actions to navigate to settings

    def is_dashboard_page_opened(self):
        """
        Verify that the dashboard page is opened.
        """
        return self.is_page_opened(with_elements=True, with_url=True)


DashboardPage().navigate_to_settings()
```

<br>

---

## 3. Split logic

When you have a large number of elements on a page, it is beneficial to group related elements into separate `Group` classes.
This not only makes the `Page` class cleaner but also allows for better organization of related elements and interactions.

### Steps to Refactor

1. **Identify Logical Groups**:
   - Determine which elements are related and can be logically grouped together. For example, elements related to a form or a sidebar can be moved to their respective `Group` classes.

2. **Create `Group` Classes**:
   - Define new `Group` classes to encapsulate these elements. Each `Group` class should inherit from a base class, similar to `Page`, and should initialize its elements.

3. **Link Group Classes to the `Page` Class**:
   - In the `Page` class, add attributes that link to instances of the `Group` classes. This keeps the `Page` class organized and provides access to the grouped elements.

### Example

Below is an example demonstrating how to refactor a `Page` class by moving elements into separate `Group` classes:

```python
from mops.base.page import Page
from mops.base.group import Group
from mops.base.element import Element


class Header(Group):
    def __init__(self):
        super().__init__(...)

    notifications_icon = Element('#header-notifications', name='Header Notifications Icon')
    user_profile_button = Element('#header-profile', name='Header User Profile')
    search_box = Element('#header-search', name='Header Search Box')

    def navigate_to_settings(self):
        """
        Navigate to the settings page.
        """
        self.user_profile_button.click()


class DashboardPage(Page):

    def __init__(self):
        super().__init__(...)

    # Sections
    header = Header()

    # Footer Controls
    footer_logout_button = Element('#footer-logout', name='Footer Logout Button')
    footer_help_link = Element('#footer-help', name='Footer Help Link')
    footer_contact_us = Element('#footer-contact', name='Footer Contact Us')

    # Main Content Controls
    main_content_title = Element('#main-title', name='Main Content Title')
    main_content_body = Element('#main-body', name='Main Content Body')

    def is_dashboard_page_opened(self):
        """
        Verify that the dashboard page is opened.
        """
        return self.is_page_opened(with_elements=True, with_url=True)


DashboardPage().header.navigate_to_settings()
# or
Header().navigate_to_settings()
```