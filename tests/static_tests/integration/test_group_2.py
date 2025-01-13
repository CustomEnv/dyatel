from mops.base.element import Element
from mops.base.group import Group


class MainGroup(Group):

    def __init__(self, custom_locator='MainGroup'):
        super().__init__(custom_locator)

    el1 = Element('lcoator')
    el2 = Element('lcoator', parent=el1)


class Nested1(MainGroup):

    def __init__(self):
        super().__init__(custom_locator='Nested1')


class Nested2(MainGroup):

    def __init__(self):
        super().__init__(custom_locator='Nested2')


def test_group_2_parent_arg_in_other_group_updated(mocked_selenium_driver):
    nested1 = Nested1()
    nested2 = Nested2()
    assert nested1.el2.parent.__base_obj_id == nested2.el1.__base_obj_id
    assert nested1.el2.parent.parent == nested1

    assert nested2.el2.parent.__base_obj_id == nested2.el1.__base_obj_id
    assert nested2.el2.parent.parent == nested2
