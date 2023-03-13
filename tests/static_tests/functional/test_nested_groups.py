import pytest

from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.base.page import Page
from tests.static_tests.conftest import all_drivers, all_ids


class Group1(Group):
    def __init__(self, locator='group1'):
        super().__init__(locator=locator)

    shared_element = Element('element', name='element')


class Group2(Group1):
    def __init__(self):
        super().__init__('group2')


class Page1(Page):
    def __init__(self):
        self.group1 = Group1()
        self.group2 = Group2()
        super().__init__('page1')


@pytest.mark.parametrize('driver', all_drivers, ids=all_ids)
def test_object_in_nested_groups(driver, request):
    request.getfixturevalue(driver)
    page = Page1()
    assert page.group1.shared_element != page.group2.shared_element
    assert page.group1.shared_element.parent != page.group2.shared_element.parent
    assert page.group1.shared_element.parent.__class__ == Group1
    assert page.group2.shared_element.parent.__class__ == Group2
