from selenium_master.base.base_element import BaseElement
from selenium_master.core.core_element import CoreElement
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement


elements_objects = (WebElement, MobileElement, CoreElement, BaseElement)


class Group(BaseElement):

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        for element in self.child_elements:
            element.parent = self
