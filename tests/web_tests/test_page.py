import pytest
from selenium.common import TimeoutException as SeleniumTimeoutException
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutException

from tests.adata.pages.mouse_event_page import MouseEventPageWithUnexpectedWait


@pytest.mark.parametrize('with_elements_case', (True, False), ids=['with elements', 'without elements'])
def test_page_elements_loaded_positive(mouse_event_page, with_elements_case):
    mouse_event_page.wait_page_loaded()
    assert mouse_event_page.is_page_opened(with_elements=with_elements_case)


@pytest.mark.parametrize('with_elements_case', (True, False), ids=['with elements', 'without elements'])
def test_page_elements_loaded_negative_with_elements(mouse_event_page, with_elements_case):
    page = MouseEventPageWithUnexpectedWait()
    try:
        page.wait_page_loaded(timeout=0.1)
    except (SeleniumTimeoutException, PlaywrightTimeoutException):
        if with_elements_case:
            assert not page.is_page_opened(with_elements=with_elements_case)
        else:
            assert page.is_page_opened(with_elements=with_elements_case)
    else:
        raise pytest.fail('Unexpected behavior. Case not covered')
