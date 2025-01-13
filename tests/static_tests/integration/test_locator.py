import pytest

from mops.base.element import Element
from mops.base.group import Group
from mops.mixins.objects.locator import Locator
from mops.utils.selector_synchronizer import get_platform_locator
from tests.static_tests.conftest import mobile_ids, mobile_drivers, desktop_drivers, desktop_ids, mocked_ios_driver


ios_locator = 'ios_locator'
android_locator = 'android_locator'
mobile_locator = 'mobile_locator'


class ExtendedClass(Group):
    def __init__(self, locator='group1', name='group1'):
        super().__init__(locator=f'{locator} updated', name=name)


class SomeGroup(Group):
    def __init__(self):
        super().__init__(Locator('default_group', mobile='mobile_group'))

    link_to_class = ExtendedClass('some locator', name='nested element')  # all elements initialised two times

    multiple_element_partial = Element(
        Locator(desktop='desktop_locator', mobile=mobile_locator),
        name='multiple element all'
    )
    multiple_element_all = Element(
        Locator(desktop='desktop_locator', ios=ios_locator, android=android_locator),
        name='multiple element all'
    )


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_link_to_class_locator_mobile(driver, request):
    request.getfixturevalue(driver)
    assert SomeGroup().link_to_class.locator == '[id="some locator updated"]'


@pytest.mark.parametrize('driver', desktop_drivers, ids=desktop_ids)
def test_link_to_class_locator_desktop(driver, request):
    request.getfixturevalue(driver)
    assert 'some locator updated' in SomeGroup().link_to_class.locator


def test_multiple_locator_ios1(mocked_ios_driver):
    assert ios_locator in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'mobile_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_android(mocked_android_driver):
    assert android_locator in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'mobile_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_selenium(mocked_selenium_driver):
    assert 'desktop_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'default_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_playwright(mocked_play_driver):
    assert 'desktop_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'default_group' in get_platform_locator(SomeGroup())


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_multiple_locator_mobile(driver, request):
    request.getfixturevalue(driver)
    assert mobile_locator in get_platform_locator(SomeGroup().multiple_element_partial)


@pytest.mark.parametrize('driver', mobile_drivers, ids=mobile_ids)
def test_multiple_locator_all_with_mobile_fallback(driver, request):
    request.getfixturevalue(driver)
    locator = get_platform_locator(
        Element(
            Locator(
                android=android_locator,
                ios=ios_locator,
                mobile=mobile_locator,
            ),
            name='multiple element broken all'
        )
    )
    expected_locator = ios_locator if driver == mocked_ios_driver.__name__ else android_locator

    assert expected_locator in locator


def test_multiple_locator_ios_with_mobile_fallback(mocked_ios_driver):
    assert ios_locator in  get_platform_locator(
        Element(Locator(ios=ios_locator, mobile=mobile_locator), name='multiple element broken ios')
    )


def test_multiple_locator_android_with_mobile_fallback(mocked_android_driver):
    assert android_locator in get_platform_locator(
        Element(Locator(android=android_locator, mobile=mobile_locator), name='multiple element broken android')
    )
