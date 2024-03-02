# Dyatel Changelog


---

## v2.1.9
*Release date: 2024-02-22*

### Added
- `Element.size` method
- `Element.location` method
- `DriverWrapper.assert_screenshot` method
- `DriverWrapper.sofr_assert_screenshot` method
- `Element.wait_element_size` method
- `DriverWrapper.wait` method
- `DriverWrapper/Element.screenshot_image` method

### Changed 
- `DriverWrapper/Element.screenshot_base` method now return image binary
- `DriverWrapper/Element.save_screenshot` method now saves screenshot and moved to base class


---

## v2.1.9
*Release date: 2024-02-22*

### Added
- Playwright `context.tracing` support

---

## v2.1.8
*Release date: 2024-01-04*

### Added
- Playwright `new_context` args supports

---

## v2.1.7
*Release date: 2023-12-05*

### Added
- VisualComparison: Dynamic threshold calculation

---

## v2.1.6
*Release date: 2023-11-26*

### Fixed
- Performance fixes for session with 2 or more browser windows

---

## v2.1.5
*Release date: 2023-10-17*

### Fixed
- Typo fix inside `MobileDriver`

---

## v2.1.4
*Release date: 2023-10-16*

### Fixed
- Internal usage of Element class inside DriverWrapper

### Changed
- AssertionError output of visual comparison

### Added
- Soft visual reference generation
- Soft assert screenshot
- `LogLevel` class

---

## v2.1.3
*Release date: 2023-09-10*

### Changed
- Selenium/Appium only: Additional logging for element enabled
- Selenium/Appium element gathering and exceptions reworked

---

## v2.1.2
*Release date: 2023-09-07*

### Fixed
- Additional logging for element disabled 

---

## v2.1.1
*Release date: 2023-09-07*

### Fixed
- `setup.py` packages 

---

## v2.1.0
*Release date: 2023-09-07*

### Added
- Abstract classes and methods
- `DriverWrapperSessions` class
- `DriverWrapper.browser_name` attribute
- Inheritance validation
- `Element.scroll_into_view` 'block' argument validation
- Selenium/Appium only: additional warning for `element` errors 

### Fixed
- Type annotations for some methods

### Changed
- `Page.anchor` property now instance attribute
- Some methods moved to subclasses
- Internal `Logging` reworked
- `DriverWrapper` from previous object reworked

---

## v2.0.0
*Release date: 2023-04-06*

### Added
- `element.wait_enabled` method
- `element.wait_disabled` method
- `element.is_enabled` method
- `VisualComparison.default_delay` property
- `VisualComparison.default_threshold` property
- `DriverWrapper.switch_to_alert` method (Selenium Only)
- `DriverWrapper.accept_alert` method (Selenium Only)
- `DriverWrapper.dismiss_alert` method (Selenium Only)
- `MobileDriver.click_in_alert` method (Appium Only)

### Fixed
- MRO for Mobile + Desktop session
- Rapidly requests for current context on mobile
- `element.all_elements` recursion
- logging stderr to stdout

### Changed
- Checkbox class removed (all methods in Element class)
- New screenshot comparison engine. By: [@laruss](https://github.com/laruss)
- Elements initialization
- `element.wait_clickable` renamed to `element.wait_enabled`
- `__repr__` for Element/Group/Page
- Driver with index will be added to logs always

---

## v1.3.4
*Release date: 2023-01-17*

### Fixed
- Error logs fixes

---

## v1.3.3
*Release date: 2023-01-12*

### Changed
- `element.assert_screenshot` elements removal rework

---

## v1.3.2
*Release date: 2022-12-08*

### Added
- mobile `element.hide_keyboard` method added
- `fill_background` arg in `element.assert_screenshot`

### Changed
- ios safaridriver support removed
- reruns disabling for visual tests without references

### Fixed
- Pillow warning fixes
- other fixes and improvements

---

## v1.3.1
*Release date: 2022-12-02*

### Added
- `element.wait_element_hidden_without_error` method
- `element.assert_screenshot` hard reference generation support
- `element.assert_screenshot` soft reference generation fix
- `element.hover` silent argument

### Changed
- Reworked wait argument for `element`: False - wait element hidden; True - wait element visible
- `page.is_page_opened` without url support
- selenium - tags (locator type) updated

### Fixed
- DifferentDriverWrapper and elements initialization fixes

---

## v1.3.0
*Release date: 2022-10-18*

### Added 
- `driver_wrapper.get_inner_window_size` method
- `driver_wrapper.switch_to_frame` method for selenium based driver
- `driver_wrapper.switch_to_parent_frame` method for selenium based driver
- `driver_wrapper.switch_to_default_content` method for selenium based driver
- `driver_wrapper.delete_cookie` method for selenium/appium based driver
- `element.is_visible` method 
- `element.is_fully_visible` method
- `element.__repr__`, `checkbox.__repr__`, `group.__repr__`, `page.__repr__` 
- `scroll_into_view` before `element.click_into_center/hover/etc.` if element isn't visible
- `name_suffix` arg for `element.assert_screenshot` 
- Auto implemented `driver` in hidden object (function/property etc.) for `element/checkbox/group/page`
- Auto implemented `parent` in hidden object (function/property etc.) for `element/checkbox`
- Platform specific locator by object kwargs: ios/android/mobile/desktop

### Changed
- `element.get_rect` for selenium desktop
- All visual comparisons staff moved to `VisualComparison` class 
- Logging

### Fixed
- `get_object_kwargs` function
- `initialize_objects_with_args` function
- `element.assert_screenshot` driver name for remote
- Click by location after scroll

---

## v1.2.8
*Release date: 2022-09-20*

### Added 
- `driver_wrapper.is_native_context` property on mobile
- `driver_wrapper.is_web_context` property on mobile
- `driver_wrapper.visual_reference_generation` that disable AssertionError exception in `element.assert_screenshot`
- `ElementNotInteractableException` handler in `element.click`

### Changed
- `element.get_rect` output value sorting
- `PlayDriver`/`CoreDriver` class variables moved to `DriverWrapper`
- `os.environ['visual']` changed to `driver_wrapper.visual_regression_path`
- `element.wait_element` exception message
- Mobile: Finding elements in native context now skips parent

### Fixed
- `autolog` params
- `driver_wrapper.switch_to_tab` with default params

---

## v1.2.6/7
*Release date: 2022-09-15*

### Fixed
- screenshot name generation

---

## v1.2.5
*Release date: 2022-09-13*

### Added
- `element.click_into_center` method
- `driver_wrapper.click_by_coordinates` method

### Fixed
- `calculate_coordinate_to_click` calculation
- Shared object of groups become unique for each class

---

## v1.2.4
*Release date: 2022-09-08*

### Added
- `assert_screenshot()` elements removal

---

## v1.2.3
*Release date: 2022-09-02*

### Fixed
- `element.is_displayed()` exception handler

---

## v1.2.1/2
*Release date: 2022-08-31*

### Fixed
- Annotations

---

## v1.2.0
*Release date: 2022-08-31*

### Added
- [Allure Screen Diff Plugin](https://github.com/allure-framework/allure2/blob/master/plugins/screen-diff-plugin/README.md) support
- Driver specific logs 
- Custom exceptions
- Screenshot name generation in `assert_screenshot`
- `KeyboardKeys` class
- `element.send_keyboard_action` method

### Changed
- `get_text` property become `text`
- `get_value` property become `value`
- `get_screenshot_base` property become `screenshot_base`
- `get_inner_text` property become `inner_text`
- `by_attr` arg of `Checkbox` removed
- `calculate_coordinate_to_click` now calculate coordinates from element location

### Fixed
- Reduced count of `find_element` execution
- Page `driver_wrapper` getter exception

---

## v1.1.1
*Release date: 2022-08-10*

### Added
- iOS SafariDriver basic support 
- Different second driver support (for mobile/desktop safari)
- Tabs manipulating methods for desktop in `CoreDriver/PlayDriver`
- Context manipulating methods for mobile in `MobileDriver`
- [pytest-rerunfailures](https://pypi.org/project/pytest-rerunfailures/#pytest-rerunfailures) support
- Type annotations for most of code
- Auto `locator_type` support for `com.android` locator 
- `element.hover` support on mobiles
- `element.hover_outside` method, that moves pointer outside from current position
- `page.swipe(_up/_down)` methods for mobile  
- Default cookie path/domain in `driver_wrapper.set_cookie` method

### Changed
- `Driver` becomes `DriverWrapper` for more readability
- Mixins classes renamed and moved to `dyatel.mixins` folder
- Selenium `core_element.wait_element` now using `is_displayed`
- Selenium exception stacktrace reduced in most cases

### Fixed
- Custom `driver_wrapper`/`driver` for child elements
- Selenium `KeyError` of `driver_wrapper.set_cookie` without `domain` 
- Driver creation with function scope of pytest

---

## v1.1.0
*Release date: 2022-07-23*

### Added
- `Checkbox` class for Playwright and Selenium 
- `set_text` method in `Element` class
- `wait_elements_count` method in `Element` class
- `wait_element_text` method in `Element` class
- `wait_element_value` method in `Element` class
- `driver_wrapper` arg for `Group` and `Page`

### Changed
- Page/Group `set_driver` workflow
- `CorePage` and `PlayPage` methods moved to `Page` 

---

## v1.0.5
*Release date: 2022-07-10*

### Added
- `_first_element` property in `PlayElement`

### Changed
- `element` property replaced with `_first_element` for elements interactions
- `parent` nesting of `Element` changed from one level to endless
- `PlayElement` / `CoreElement` initialization

### Fixed
- `all_elements` execution time/nesting

---

## v1.0.4
*Release date: 2022-07-07*

### Added
- `set_driver` function for page object
- Multiple drivers support

### Changed
- Drivers initialization
- `driver`, `driver_wrapper` become property methods
