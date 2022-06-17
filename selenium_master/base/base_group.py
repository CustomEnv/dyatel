from selenium_master.base.base_element import BaseElement
from selenium_master.core.core_element import CoreElement
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement


elements_objects = (WebElement, MobileElement, CoreElement, BaseElement)


class Group(BaseElement):

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        for element in self._get_group_elements():
            if not element.driver:
                element.__init__(element.locator, name=element.name)
            element.parent = self

    def _get_group_elements(self):
        """Return page elements and page objects of this page object

        :returns: list of page elements and page objects
        """
        page_elements = []
        for attribute, value in list(self.__class__.__dict__.items()):
            if isinstance(value, elements_objects):
                page_elements.append(value)
        return page_elements
