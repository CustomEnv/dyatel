import pytest


@pytest.mark.xfail_platform('playwright', 'appium', reason='Implementation required')
def test_switch_to_frame(driver_wrapper, frames_page):
    assert frames_page.anchor.is_displayed()

    driver_wrapper.switch_to_frame(frames_page.frame1)
    assert not frames_page.anchor.is_displayed()
    assert frames_page.frame1.button.text == 'Click Me 1'
    assert frames_page.frame1.button.click().text == 'Clicked'

    driver_wrapper.switch_to_frame(frames_page.frame2)
    assert frames_page.frame2.button.text == 'Click Me 2'
    assert frames_page.frame2.button.click().text == 'Clicked'

    driver_wrapper.switch_to_parent_frame()

    driver_wrapper.switch_to_frame(frames_page.frame3)
    assert not frames_page.frame3.button.is_displayed()

    driver_wrapper.switch_to_frame(frames_page.frame4)
    assert frames_page.frame4.button.text == 'Click Me 4'
    assert frames_page.frame4.button.click().text == 'Clicked'

    driver_wrapper.switch_to_default_content()

    assert frames_page.anchor.is_displayed()
