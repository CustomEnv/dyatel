import pytest

from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


def get_class_static(class_object):
    all_static = list(dict(class_object.__dict__.items()).keys())
    return sorted(filter(None, [item if not item.startswith('_') else None for item in all_static]))


def test_playwright_and_selenium_page_compatibility():
    assert get_class_static(PlayPage) == sorted(get_class_static(WebPage) + get_class_static(CorePage))


def test_playwright_and_selenium_element_compatibility():
    assert get_class_static(PlayElement) == sorted(get_class_static(WebElement) + get_class_static(CoreElement))


def test_selenium_mobile_and_web_element_compatibility():
    web_static = sorted(get_class_static(WebElement) + get_class_static(CoreElement))
    mobile_static = sorted(get_class_static(MobileElement) + get_class_static(CoreElement))
    assert web_static == mobile_static


def test_selenium_mobile_and_web_page_compatibility():
    web_static = sorted(get_class_static(WebPage) + get_class_static(CorePage))
    mobile_static = sorted(get_class_static(MobilePage) + get_class_static(CorePage))
    assert web_static == mobile_static
