# Dyatel Changelog

---
## v1.2.0
*Release date: In development*

### Added
- [Allure Screen Diff Plugin](https://github.com/allure-framework/allure2/blob/master/plugins/screen-diff-plugin/README.md) support
- Driver specific logs 
- Custom exceptions
- Screenshot name generation in `assert_screenshot`
- `KeyboardKeys` class

### Changed
- `get_text` property become `text`
- `get_value` property become `value`
- `get_screenshot_base` property become `screenshot_base`
- `get_inner_text` property become `inner_text`
- `by_attr` arg of `Checkbox` removed
- `calculate_coordinate_to_click` now can calculate coordinates from element location

### Fixed
- Reduced count of `find_element` execution 

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
