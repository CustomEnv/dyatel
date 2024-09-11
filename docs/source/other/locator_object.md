# Locator Object

## Overview

The `Locator` class is designed to provide a flexible mechanism for managing locators in a unified way.
This class supports different locator types for various platforms and devices, including `desktop`, `mobile`, and `tablet` environments. 
The `Locator` class is particularly useful in automation frameworks where locators need to be adapted based on the specific driver 
and capabilities being used.

This object and its usage aim to reduce the redundancy of creating multiple attributes for different platforms. 
By centralizing locators in a single `Locator` object, it simplifies the codebase and enhances maintainability.

<br>

## Interface

```{eval-rst}  
.. autoclass:: dyatel.mixins.objects.locator.Locator
   :members: 
   
   .. attribute:: default: Optional[str] = None
      -   the default locator for the object. This is used if no other locators are specified or if no specific platform/device type is detected.
   
   .. attribute:: loc_type: Optional[str] = None
      -   selenium & Appium only: specifies the type of locator (e.g., `By.CSS_SELECTOR`, `By.XPATH`, etc.). This attribute is optional and, if not provided, the locator type will be selected automatically based on the provided locator.
   
   .. attribute:: desktop: Optional[str] = None
      -   the locator for desktop environments. This can be used for browsers on desktop platforms.
   
   .. attribute:: mobile: Optional[str] = None
      -   the locator for general mobile environments. This is used for mobile platforms other than iOS and Android and for mobile resolution of desktop browser.
   
   .. attribute:: tablet: Optional[str] = None
      -   appium only: The locator specifically for tablet devices. Useful for web and app automation on tablet devices. The `is_tablet: True` capability required.
   
   .. attribute:: ios: Optional[str] = None
      -   appium only: The locator specifically for iOS devices. This attribute allows for targeting locators specific to iOS applications.
   
   .. attribute:: android: Optional[str] = None
      -   appium only: The locator specifically for Android devices. This attribute allows for targeting locators specific to Android applications.
   
```

<br>

## Usage

The `Locator` class is designed to be flexible and adaptive, making it suitable for various automation scenarios. 
Here’s how the attributes work together:

- **`loc_type`** is optional. If not specified, the system will attempt to automatically select the appropriate locator type based on the provided locator.
- **`default`** will be used if no specific locator is provided for the current platform or device.

<br>

### Example

```python
# Providing string parameter instead of Locator object
button = Element('.button', name='button')

search_button = Element(Locator(desktop='.search', mobile='.mobile.search'), name='search button')
```