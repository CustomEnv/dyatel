# Element Key Features

```{note}
Here you will find information on complex or ambiguous functionality.
For a comprehensive list of all available methods, 
please refer to the {doc}`Element Interface <./interface>` documentation.
```

<br>

## 1. Delayed Element initialization:

```{important}
Following information suitable for `Element` object, that defined as class attribute of `Page` or `Group`
```

**Key functionality:**
- Elements are initialized based on the current driver. If no driver is available, the element will be initialized later within the `Page` or `Group` class initialisation.
- The `driver` and `driver_wrapper` will sets to `Element` object automatically from `Page` or `Group` instances


---

<br>

## 2. Custom waits
The waiting methods for _Selenium_ and _Appium_ have been reworked to improve efficiency, 
particularly for negative checks (i.e., when an element is not present on the page).

**Key changes:**
- Reduced `implicitly_wait`: The default implicitly_wait time in _Selenium_ and _Appium_ has been reduced. This adjustment is made because Selenium's `implicitly_wait` tends to cause long delays when checking for elements that are not present on the page.
- Internal Waiting Mechanism: Instead of relying on _Selenium's_ or _Appium's_ native waiting strategies, all waiting methods now use internal methods with built-in Python loops. This allows for more precise control over the waiting time and conditions, leading to faster and more reliable checks.

---

<br>


## 3. Built-in waits
Most methods automatically wait for specific element states.
For example, the framework will wait until a web element becomes clickable before executing `click` method on it.
