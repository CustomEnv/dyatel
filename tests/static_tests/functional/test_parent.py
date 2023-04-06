import pytest

from dyatel.base.element import Element
from dyatel.base.group import Group
from tests.static_tests.conftest import selenium_drivers, selenium_ids


class Section(Group):
    def __init__(self):
        super().__init__('Section')

    elwp = Element('elwp')
    elwoutp = Element('elwoutp', parent=False)
    elwithop = Element('elwithop', parent=elwp)


@pytest.mark.parametrize('driver', selenium_drivers, ids=selenium_ids)
def test_element_with_parent(driver, request):
    request.getfixturevalue(driver)
    section = Section()
    assert section.elwp.parent == section
    assert section.elwithop.parent.parent == section
    assert section.elwoutp.parent is False
    assert section.elwithop.parent.locator in section.elwp.locator
    assert section.elwithop.parent._initialized
