# Element

```{toctree}
---
hidden:
---

key_features
best_practices
interface
```

## Overview

The Element class serves as a fundamental building block for constructing user interface (UI) components.
It acts as a wrapper around _Selenium WebElement_, _Appium WebElement_, and _Playwright Locator_ objects, 
offering additional utility methods and abstractions to facilitate interaction with web page elements within the 
Page Object Model (POM) and Page Component Object Model (PCOM) patterns.

<br>

### Core Benefits & Rules

1. **Simplified web element interactions:**
   - `Element` methods provide a cleaner way to interact with web page element.

2. **Enhanced wait mechanisms:**
   - Built-in methods simplify web page element interaction waiting. For _Selenium_ and _Appium_, using custom waits is generally preferred over implicit waits, especially for negative checks, as implicit waits can be slow in such scenarios.

3. **Delayed initialization**:
   - The `Element` object has a delayed initialization within the `Group` or `Page` classes, where it is defined.

4. **Attribute-based usage**:
   - Unlike `Group` or `Page` objects, which can be used as classes, `Element` objects should be defined as attributes. This approach promotes better code organization and reusability.

<br>
 
This section covers features and behaviour of `Element` class detail:
- {doc}`Element Initialisation <../other/objects_initialisation>`
- {doc}`Element Key Features <./key_features>`
- {doc}`Element Best Practices <./best_practices>`
- {doc}`Element Interface <./interface>`
