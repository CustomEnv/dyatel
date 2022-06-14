import os

from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement


class BaseElement(MobileElement, WebElement):
    def __init__(self, *args, **kwargs):
        if os.environ.get('mobile', default=False):
            super(MobileElement, self).__init__(*args, **kwargs)
        else:
            super(WebElement, self).__init__(*args, **kwargs)
