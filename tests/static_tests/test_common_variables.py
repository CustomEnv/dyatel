import pytest
from selenium.webdriver.common.by import By

from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.mixins.internal_utils import all_tags


tags = all_tags + ['header h4']


@pytest.mark.parametrize('locator', ('.element', '[id *= element]'))
@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_base_class_auto_css_locator(locator, base_class):
    assert base_class(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator(locator):
    assert WebElement(locator).locator_type == By.TAG_NAME


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator_mobile(locator):
    assert MobileElement(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', ('//a', '/b', '//*[@contains(@class, "name") and .="name"]'))
@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_base_class_auto_xpath_locator(locator, base_class):
    assert base_class(locator).locator_type == By.XPATH


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id'))
def test_base_class_auto_id_locator_web(locator):
    assert WebElement(locator).locator_type == By.ID


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id', 'com.android.chrome:id/bottom_container'))
def test_base_class_auto_id_locator_mobile(locator):
    assert MobileElement(locator).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_specify_css_locator_type(base_class):
    assert base_class('[href="/loaddelay"]', locator_type=By.CSS_SELECTOR).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_mobile(locator):
    assert WebElement(locator, locator_type=By.CLASS_NAME).locator_type == By.CLASS_NAME


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_web(locator):
    assert MobileElement(locator, locator_type=By.CLASS_NAME).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_name_missed(base_class):
    locator = '.sample .locator'
    assert base_class(locator).name == locator


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_name_specified(base_class):
    locator, name = '.sample .locator', 'sample name'
    assert base_class(locator, name=name).name == name
