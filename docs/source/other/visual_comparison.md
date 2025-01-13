# Visual Comparison 

## Overview

```{attention}
Supported for `allure` and `pytest` frameworks.
- `allure` for reporting;
- `pytest` for sreenshot name definition.
```

The `VisualComparison` class is designed to facilitate visual regression testing by comparing screenshots of UI 
elements across different runs. It supports screenshot capturing, comparison, and visual difference highlighting. 
The class also handles dynamic thresholds, image comparison metrics, and can generate visual references for testing purposes.

<br>

## Interface

```{eval-rst}  
.. autoclass:: mops.visual_comparison.VisualComparison 
   :exclude-members: calculate_threshold 
   :members: assert_screenshot
   
   .. attribute:: visual_regression_path: str = ''
      -   Path where visual regression images (reference, output, and diff) will be stored. 
   
   .. attribute:: test_item: pytest.Item = None
      -   The pytest `request.node.` object associated with the visual comparison.
   
   .. attribute:: attach_diff_image_path: bool = False
      -   Flag to determine whether to attach the diff image path to the report. 
   
   .. attribute:: skip_screenshot_comparison: bool = False
      -   If set to `True`, the screenshot comparison will be skipped. 
   
   .. attribute:: visual_reference_generation: bool = False
      -   Enables generation of visual references. 
   
   .. attribute:: hard_visual_reference_generation: bool = False
      -   Forces generation of visual references, replacing existing ones. 
   
   .. attribute:: soft_visual_reference_generation: bool = False
      -   Allows generation of visual references only if they do not exist. 
   
   .. attribute:: default_delay: Union[int, float] = 0.75
      -   Default delay before taking a screenshot. 
   
   .. attribute:: default_threshold: Union[int, float] = 0
      -   Default threshold for image comparison. 
   
   .. attribute:: dynamic_threshold_factor: int = 0
      -   Factor for dynamically calculating threshold based on image size. 
   
   .. attribute:: diff_color_scheme: tuple = (0, 255, 0)
      -   Color scheme used for highlighting differences in images. 
```

<br>

## Usage

Usage
The `assert_screenshot` method of the `VisualComparison` class is utilized indirectly through the `assert_screenshot`
and `soft_assert_screenshot` methods provided by the `Group`, `Element`, and `DriverWrapper` classes. 
These methods are designed to take screenshots of elements or pages and compare them against a reference image to 
validate visual consistency across tests.

<br>

## Allure Integration
If the Allure framework is available in the project, the results of the visual comparison will be automatically 
attached to the Allure report as part of the test case. This includes:

**Actual Screenshot:**
   - The screenshot taken during the test.

**Expected Screenshot:**
   - The reference image used for comparison.

**Difference Screenshot:**
   - An image highlighting any differences found between the actual and expected screenshots.
