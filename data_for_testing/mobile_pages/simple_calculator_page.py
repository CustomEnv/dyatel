from appium.webdriver.common.appiumby import AppiumBy
from selenium_master.driver.core_driver import CoreDriver
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.pages.mobile_page import MobilePage


class CalculatorPage(MobilePage):
    """ Calculator main page: correspond to android and ios app """

    def __init__(self):
        locator_type, locator = AppiumBy.XPATH, '//*[@text="TestingBotSample"]'  # Android locator

        if CoreDriver.is_ios:
            locator_type, locator = AppiumBy.ACCESSIBILITY_ID, 'Home'

        super(CalculatorPage, self).__init__(locator_type, locator, name='Calculator page')

    @property
    def input_a(self):
        return MobileElement(AppiumBy.ACCESSIBILITY_ID, 'inputA', name='input A')

    @property
    def input_b(self):
        return MobileElement(AppiumBy.ACCESSIBILITY_ID, 'inputB', name='input B')

    @property
    def input_sum(self):
        locator = 'total' if CoreDriver.is_ios else 'sum'
        return MobileElement(AppiumBy.ACCESSIBILITY_ID, locator, name='input summary')
