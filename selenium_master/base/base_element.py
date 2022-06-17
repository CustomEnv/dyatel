from selenium_master.core.core_driver import CoreDriver
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement


class BaseElement(MobileElement, WebElement):
    def __init__(self, *args, **kwargs):
        if CoreDriver.mobile:
            self.root_element_class = MobileElement
            super(MobileElement, self).__init__(*args, **kwargs)
        else:
            self.root_element_class = WebElement
            super(WebElement, self).__init__(*args, **kwargs)
