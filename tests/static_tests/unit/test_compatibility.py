import inspect

import pytest

from dyatel.abstraction.driver_wrapper_abc import DriverWrapperABC
from dyatel.abstraction.element_abc import ElementABC
from dyatel.abstraction.page_abc import PageABC
from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.base.page import Page
from dyatel.dyatel_play.play_driver import PlayDriver

from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.dyatel_sel.driver.mobile_driver import MobileDriver
from dyatel.dyatel_sel.driver.web_driver import WebDriver
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


def get_methods_and_names(_class):
    result = {}

    for name, member in inspect.getmembers(_class):
        if not name.startswith('_') and f' {_class.__name__}.{name}' in str(member):
            if inspect.ismethod(member) or inspect.isfunction(member):
                result[name] = member
            elif isinstance(member, property):
                result[name] = member

    return result


def get_signature(_func):
    return str(inspect.signature(_func).parameters).replace('"', '').replace("'", '')

def get_signature_additional(_func):
    """ Useful for checking * in methods arguments """
    return str(inspect.signature(_func)).split(' ->')[0]


def compare_methods_bulk(_class, _abc, _main_class):
    """
    Compares all methods of two classes and checks if they are identical.
    Returns a dictionary with method names as keys and comparison results as values.
    """
    results = {}

    # Get all methods from both classes
    cls1_methods = get_methods_and_names(_class)
    cls2_methods = get_methods_and_names(_abc)
    assert cls1_methods
    assert cls2_methods

    # Find common methods
    common_methods = set(cls1_methods.keys()).intersection(cls2_methods.keys())

    for method in common_methods:
        func1 = cls1_methods[method]
        func2 = cls2_methods[method]

        # Compare signatures
        if inspect.isfunction(func1):
            if not inspect.isfunction(func2):
                results[method] = "Function type do not match"

            if get_signature(func1) != get_signature(func2):
                results[method] = "Signatures do not match"

            if get_signature_additional(func1) != get_signature_additional(func2):
                results[method] = "Additional signatures do not match"

        if isinstance(func1, property):
            if not isinstance(func2, property):
                results[method] = "Property type do not match"

        if method != 'element' or _class is _main_class:
            class_func_doc = inspect.getdoc(func1)
            abc_class_func_doc = inspect.getdoc(func2).replace(_main_class.__name__, _class.__name__)
            if class_func_doc != abc_class_func_doc:
                results[method] = "Docstrings do not match"

    # Check for methods not in common
    only_in_cls1 = set(cls1_methods.keys()) - common_methods
    for method in only_in_cls1:
        results[method] = f"Only in {_class.__name__}"

    assert not results, f'{_class.__name__} & {_abc.__name__} methods missmatch: {results}'


@pytest.mark.parametrize('base_class', [Element, WebElement, CoreElement, MobileElement, PlayElement])
def test_element_to_abc(base_class):
    compare_methods_bulk(base_class, ElementABC, Element)


@pytest.mark.parametrize('base_class', [Page, MobilePage])
def test_page_to_abc(base_class):
    compare_methods_bulk(base_class, PageABC, Page)


@pytest.mark.parametrize('base_class', [DriverWrapper, CoreDriver, WebDriver, MobileDriver, PlayDriver])
def test_driver_wrapper_to_abc(base_class):
    compare_methods_bulk(base_class, DriverWrapperABC, DriverWrapper)


@pytest.mark.parametrize('base_class', [WebPage, CorePage, PlayPage])
def test_empty_pages(base_class):
    """
    Test relevant, when base_class are empty and does not contain any members
    When base_class is not empty it should be moved to test_page_to_abc
    """
    assert not get_methods_and_names(base_class)

