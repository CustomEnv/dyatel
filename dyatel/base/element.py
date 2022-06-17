from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement


class Element(MobileElement, WebElement):
    def __init__(self, *args, **kwargs):
        if CoreDriver.mobile:
            self.root_element_class = MobileElement
            super(MobileElement, self).__init__(*args, **kwargs)
        else:
            self.root_element_class = WebElement
            super(WebElement, self).__init__(*args, **kwargs)
