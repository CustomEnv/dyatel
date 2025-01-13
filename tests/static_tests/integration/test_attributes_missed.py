from mops.base.element import Element
from mops.base.group import Group
from mops.base.page import Page


class Section1(Group):
    def __init__(self):
        super().__init__('Section')


class Section2(Section1):
    attr = Element('attr')


class Page1(Page):
    def __init__(self):
        super().__init__('Page1')


class Page2(Page1):

    def __init__(self):
        super().__init__()
        self.section = Section2()


def test_fixme():
    pass  # todo: case not covered
