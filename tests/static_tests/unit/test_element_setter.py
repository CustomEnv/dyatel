import pytest

from dyatel.base.element import Element
from tests.static_tests.conftest import all_drivers, all_ids


@pytest.mark.parametrize('driver', all_drivers, ids=all_ids)
def test_element_setter_negative(driver, request):
    request.getfixturevalue(driver)
    try:
        Element('').element = 'element'
    except AssertionError:
        pass
    else:
        raise AssertionError('AssertionError should be raised')
