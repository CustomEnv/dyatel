import pytest

from mops.keyboard_keys import KeyboardKeys


@pytest.mark.skip_platform('android', 'ios')
def test_keyboard_actions(keyboard_page):
    for key, key_name in ((KeyboardKeys.BACKSPACE, 'Backspace'), (KeyboardKeys.ENTER, 'Enter')):
        keyboard_page.input_area.send_keyboard_action(key)
        assert key_name in keyboard_page.key_badge.text
