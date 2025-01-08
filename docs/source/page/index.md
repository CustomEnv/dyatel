# Page

```{toctree}
---
hidden:
---

./key_features
./best_practices
./interface
```

## Overview

The `Page` class in Dyatel Wrapper is designed to act as a flexible and adaptable page object, essential for 
implementing the Page Object Model (POM). It dynamically adjusts its base class and behavior based on the underlying
driver (`PlayPage` for _playwright_, `MobilePage` for _appium_, or `WebPage` for _selenium_), allowing for consistent
and reusable page objects across different platforms.

<br>

### Core Benefits & Rules

1. **Encapsulation of Page Elements and Groups**:
   - The `Page` class allows you to define and encapsulate all the web elements and sections of a page as attributes (known as [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)). Each attribute is represented as an instance of an `Element` or `Group` class, making it easy to interact with them directly.

2. **Initialization of Elements and Groups**:
   - During the instantiation of a `Page` object, all defined elements and sections are automatically initialized. Detailed information: {doc}`Page Initialisation <../other/objects_initialisation>`

3. **Element Interactions**:
   - The `Page` class provides methods for interacting with elements, such as clicking buttons, entering text, and verifying element states. This promotes reusability and reduces duplication of interaction logic across tests.

4. **Page-Specific Methods**:
   - In addition to element interactions, the `Page` class supports defining page-specific methods that encapsulate common actions or workflows related to the page. This helps to keep test scripts clean and focused on the actions rather than on how to perform them.

<br>

This section covers features and behaviour of `Page` class detail:
- {doc}`Page Initialisation <../other/objects_initialisation>`
- {doc}`Page Key Features <./key_features>`
- {doc}`Page Best Practices <./best_practices>`
- {doc}`Page Interface <./interface>`
