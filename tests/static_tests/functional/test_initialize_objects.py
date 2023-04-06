from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.exceptions import NotInitializedException


class Section(Group):
    def __int__(self):
        super().__init__('section_test_initialize_objects')
    el = Element('el_test_initialize_objects')


class RootSection(Group):
    def __int__(self):
        super().__init__('section_1_test_initialize_objects')
    section = Section()


def test_initialize_objects(mocked_selenium_driver):
    """ covers initialize_objects function """
    root_section = RootSection()
    assert root_section._initialized
    assert root_section.section._initialized
    assert root_section.section.el._initialized
    try:
        RootSection.section.el.element
    except NotInitializedException:
        pass
    else:
        raise AssertionError('NotInitializedException should be raised')
