# Dyatel Changelog

---
## v1.1.1
*Release date: In development*

---

## v1.1.0
*Release date: 2022-22-07*

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
*Release date: 2022-10-07*

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
