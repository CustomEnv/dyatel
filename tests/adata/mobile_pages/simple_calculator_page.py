from appium.webdriver.common.appiumby import AppiumBy

from mops.base.element import Element
from mops.base.page import Page
from mops.selenium.core.core_driver import CoreDriver


class CalculatorPage(Page):
    """ Calculator main page: correspond to android and ios app """

    def __init__(self):
        locator_type, locator = AppiumBy.XPATH, '//*[@text="TestingBotSample"]'  # Android locator

        if self.driver_wrapper.is_ios:
            locator_type, locator = AppiumBy.ACCESSIBILITY_ID, 'Home'

        super(CalculatorPage, self).__init__(locator, locator_type, name='Calculator page')

    input_a = Element('inputA', AppiumBy.ACCESSIBILITY_ID, name='input A')
    input_b = Element('inputB', AppiumBy.ACCESSIBILITY_ID, name='input B')

    @property
    def input_sum(self):
        locator = 'total' if self.driver_wrapper.is_ios else 'sum'
        return Element(locator, AppiumBy.ACCESSIBILITY_ID, name='input summary')
