# Group

```{toctree}
---
maxdepth: 1
---

./key_features
./best_practices
./interface
```

## Overview

The `Group` class is a specialized `Element` that represents a collection of related elements within a web page. 
It is specifically needed for the Page Component Object Model (PCOM), providing a higher-level abstraction for 
organizing and interacting with groups of elements. This offers additional benefits over the base `Element` class,
making it easier to manage and interact with complex UI components as cohesive units.

<br>

### Core Benefits & Rules

1. **Encapsulation Elements**:
   - The `Group` class allows you to define and encapsulate all the web elements of a Group as attributes (known as [Page Component Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/#page-component-objects)). Each element is represented as an instance of an `Element` class or similar, making it easy to interact with them directly.

2. **Element Locating Context Modification**:
   - The `Group` class efficiently searches for element locators within its own context, instead of entire driver object. This enhances performance and minimizes unexpected behavior.
 
3. **Class-Based Usage**:
   - Unlike `Element` objects, which can be used as attributes, `Group` objects should be defined as classes. This approach promotes better code organization and reusability.

4. **Initialization of Elements**:
   - During the instantiation of a `Group` object, all defined attributes with instance of `Element` are automatically initialized. This ensures that elements are ready for interaction as soon as the Group object is created. Logic same as for `Page` class

<br>

This section covers features and behaviour of `Group` class detail:
- {doc}`Group Initialisation <../other/objects_initialisation>`
- {doc}`Group Key Features <./key_features>`
- {doc}`Group Best Practices <./best_practices>`
- {doc}`Group Interface <./interface>`
