from dyatel.base.group import Group
from dyatel.base.page import Page


class WrapperGroup(Group):
    pass


class SomePage(Page, WrapperGroup):
    pass


def test_unexpected_page_inheritance(mocked_selenium_driver):
    try:
        SomePage()
    except TypeError:
        pass
    else:
        raise Exception('Unexpected behaviour')


class WrapperPage(Page):
    pass


class Section(Group, WrapperPage):
    pass


def test_unexpected_element_or_group_inheritance(mocked_selenium_driver):
    try:
        Section()
    except TypeError:
        pass
    else:
        raise Exception('Unexpected behaviour')
