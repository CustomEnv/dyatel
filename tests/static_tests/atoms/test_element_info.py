from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.mixins.core_mixin import get_element_info


class SomeGroup(Group):
    def __init__(self):
        super().__init__('group')

    el = Element('element')
    mel = Element('delement', ios='ielement', android='aelement')


def test_get_element_info():
    el = Element('element')
    assert 'Selector: ["css selector": "[id="element"]"]' in get_element_info(el)


def test_get_element_info_with_parent():
    el = SomeGroup().el
    assert 'Selector: ["css selector": "[id="element"]"]. ' \
           'Parent selector: ["css selector": "[id="group"]"]' in get_element_info(el)


def test_get_element_info_with_platform(mocked_ios_driver):
    el = Element('delement', ios='ielement', android='aelement')
    assert 'Selector: ["css selector": "[id="ielement"]"]' in get_element_info(SomeGroup().mel)
