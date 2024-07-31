from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.mixins.internal_mixin import get_element_info
from dyatel.mixins.objects.locator import Locator


class SomeGroup(Group):
    def __init__(self, driver_wrapper=None):
        super().__init__(Locator('group', ios='gielement', android='gaelement'), driver_wrapper=driver_wrapper)

    el = Element('element')
    mel = Element(
        Locator('delement', ios='ielement', android='aelement')
    )


def test_get_element_info(mocked_selenium_driver):
    el = Element('element')
    assert 'Selector: ["id": "element"]' in get_element_info(el)


def test_get_element_info_with_parent(mocked_selenium_driver):
    el = SomeGroup().el
    assert 'Selector: ["id": "element"]. ' \
           'Parent selector: ["id": "group"]' in get_element_info(el)


def test_get_element_info_with_platform_ios(mocked_ios_driver):
    assert 'Selector: ["css selector": "[id="ielement"]"]. ' \
           'Parent selector: ["css selector": "[id="gielement"]"]' in get_element_info(SomeGroup().mel)


def test_get_element_info_with_platform_android(mocked_android_driver):
    assert 'Selector: ["css selector": "[id="aelement"]"]. ' \
           'Parent selector: ["css selector": "[id="gaelement"]"]' in get_element_info(SomeGroup().mel)


def test_get_element_info_with_platform_mobile_and_desktop(mocked_android_driver, mocked_selenium_driver):
    mobile_element = SomeGroup(driver_wrapper=mocked_android_driver).mel
    assert 'Selector: ["css selector": "[id="aelement"]"]. ' \
           'Parent selector: ["css selector": "[id="gaelement"]"]' in get_element_info(mobile_element)

    desktop_element = SomeGroup(driver_wrapper=mocked_selenium_driver).mel
    assert 'Selector: ["id": "delement"]. ' \
           'Parent selector: ["id": "group"]' in get_element_info(desktop_element)
