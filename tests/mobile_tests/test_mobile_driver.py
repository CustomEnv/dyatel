from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from tests.adata.pages.mouse_event_page import MouseEventPage
from tests.adata.pages.pizza_order_page import PizzaOrderPage


def test_second_driver_for_mobile_same_page_set_driver(driver_wrapper, second_driver_wrapper):
    mouse_page_mobile = MouseEventPage(driver_wrapper)  # mobile driver
    mouse_page_desktop = MouseEventPage(second_driver_wrapper)  # desktop driver
    assert len(DriverWrapper.all_drivers) == 2

    mouse_page_mobile.open_page()
    mouse_page_desktop.open_page()

    assert mouse_page_mobile.header_logo.__class__.__base__ == MobileElement
    assert mouse_page_desktop.header_logo.__class__.__base__ == WebElement
    assert mouse_page_mobile.__class__.__base__ == MobilePage
    assert mouse_page_desktop.__class__.__base__ == WebPage

    assert mouse_page_desktop.is_page_opened()
    assert mouse_page_mobile.is_page_opened()


def test_second_driver_for_mobile_driver_by_arg(driver_wrapper, second_driver_wrapper):
    pizza_page = PizzaOrderPage(driver_wrapper)  # mobile driver
    mouse_page = MouseEventPage(second_driver_wrapper)  # desktop driver
    assert len(DriverWrapper.all_drivers) == 2

    assert mouse_page.__class__.__base__ == WebPage
    assert pizza_page.__class__.__base__ == MobilePage

    mouse_page.open_page()
    pizza_page.open_page()

    assert pizza_page.driver_wrapper is not mouse_page.driver_wrapper
    assert pizza_page.driver is not mouse_page.driver
    assert mouse_page.header_logo.driver is not pizza_page.quantity_input.driver
    assert mouse_page.header_logo.driver_wrapper is not pizza_page.quantity_input.driver_wrapper

    assert mouse_page.is_page_opened()
    assert mouse_page.header_logo.is_displayed()
    assert mouse_page.header_logo.__class__.__base__ == WebElement

    assert pizza_page.is_page_opened()
    assert pizza_page.quantity_input.is_displayed()
    assert pizza_page.quantity_input.__class__.__base__ == MobileElement
