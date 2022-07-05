import pytest
from selenium.webdriver.common.by import By

from dyatel.dyatel_sel.core.core_element import CoreElement
from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.internal_utils import all_tags


tags = all_tags + ['header h4']


@pytest.mark.parametrize('locator', ('.element', '[id *= element]'))
@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_base_class_auto_css_locator(locator, base_class):
    assert base_class(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_base_class_auto_tag_name_locator(locator, base_class):
    assert base_class(locator).locator_type == By.TAG_NAME


@pytest.mark.parametrize('locator', ('//a', '/b', '//*[@contains(@class, "name") and .="name"]'))
@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_base_class_auto_xpath_locator(locator, base_class):
    assert base_class(locator).locator_type == By.XPATH


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id'))
@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_base_class_auto_id_locator(locator, base_class):
    assert base_class(locator).locator_type == By.ID


@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_specify_css_locator_type(base_class):
    assert base_class('[href="/loaddelay"]', locator_type=By.CSS_SELECTOR).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_specify_class_name_locator_type(base_class, locator):
    assert base_class(locator, locator_type=By.CLASS_NAME).locator_type == By.CLASS_NAME


@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_name_missed(base_class):
    locator = '.sample .locator'
    assert base_class(locator).name == locator


@pytest.mark.parametrize('base_class', (CorePage, CoreElement))
def test_name_specified(base_class):
    locator, name = '.sample .locator', 'sample name'
    assert base_class(locator, name=name).name == name
