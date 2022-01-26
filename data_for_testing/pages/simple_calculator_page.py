from appium.webdriver.common.mobileby import MobileBy

from selenium_master.driver.core_driver import CoreDriver
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.pages.mobile_page import MobilePage


class CalculatorPage(MobilePage):
    """ Correspond to android app page """

    def __init__(self):
        locator_type, locator = MobileBy.XPATH, '//*[@text="TestingBotSample"]'  # Android locator

        if CoreDriver.is_ios:
            locator_type, locator = MobileBy.ACCESSIBILITY_ID, 'Home'

        super(CalculatorPage, self).__init__(locator_type, locator, name='Calculator page')

    @property
    def input_a(self):
        return MobileElement(MobileBy.ACCESSIBILITY_ID, 'inputA', name='input A')

    @property
    def input_b(self):
        return MobileElement(MobileBy.ACCESSIBILITY_ID, 'inputB', name='input B')

    @property
    def input_sum(self):
        locator = 'total' if CoreDriver.is_ios else 'sum'
        return MobileElement(MobileBy.ACCESSIBILITY_ID, locator, name='input summary')
