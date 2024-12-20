import inspect

import pytest
from dyatel.abstraction.element_abc import ElementABC
from dyatel.abstraction.page_abc import PageABC
from dyatel.base.element import Element
from dyatel.base.page import Page

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

def get_methods_and_names(_class):
    result = {}

    for name, func in inspect.getmembers(_class, predicate=inspect.isfunction):
        if not name.startswith('_') and _class.__name__ in str(func):
            result[name] = func

    return result


def get_signature(_func):
    return str(inspect.signature(_func).parameters).replace('"', '').replace("'", '')


def compare_methods_bulk(_class, _abc, _main_class):
    """
    Compares all methods of two classes and checks if they are identical.
    Returns a dictionary with method names as keys and comparison results as values.
    """
    results = {}

    # Get all methods from both classes
    cls1_methods = get_methods_and_names(_class)
    cls2_methods = get_methods_and_names(_abc)

    # Find common methods
    common_methods = set(cls1_methods.keys()).intersection(cls2_methods.keys())

    for method in common_methods:
        func1 = cls1_methods[method]
        func2 = cls2_methods[method]

        # Compare signatures
        if get_signature(func1) != get_signature(func2):
            results[method] = "Signatures do not match"

        if _class is _main_class or method not in _main_class.__dict__:
            class_func_doc = inspect.getdoc(func1)
            abc_class_func_doc = inspect.getdoc(func2).replace(_main_class.__name__, _class.__name__)
            if class_func_doc != abc_class_func_doc:
                results[method] = "Docstrings do not match"

    # Check for methods not in common
    only_in_cls1 = set(cls1_methods.keys()) - common_methods
    for method in only_in_cls1:
        results[method] = f"Only in {_class.__name__}"

    assert not results, f'{_class.__name__} & {_abc.__name__} methods missmatch: {results}'

# TODO: Rework with compare_methods_bulk
def test_playwright_and_selenium_page_compatibility():
    assert sorted(get_class_static(PlayPage)) == sorted(get_class_static(WebPage) + get_class_static(CorePage))

# TODO: Rework with compare_methods_bulk
def test_playwright_and_selenium_element_compatibility():
    assert sorted(get_class_static(PlayElement)) == sorted(get_class_static(WebElement) + get_class_static(CoreElement))


@pytest.mark.parametrize('base_class', [Element, WebElement, CoreElement, MobileElement, PlayElement])
def test_element_to_abc(base_class):
    compare_methods_bulk(base_class, ElementABC, Element)


@pytest.mark.parametrize('base_class', [Page, WebPage, CorePage, MobilePage, PlayPage])
def test_page_to_abc(base_class):
    compare_methods_bulk(base_class, PageABC, Page)

