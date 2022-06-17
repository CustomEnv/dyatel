from selenium_master.base.base_element import BaseElement
from selenium_master.core.core_element import CoreElement
from selenium_master.elements.mobile_element import MobileElement
from selenium_master.elements.web_element import WebElement


class Group(BaseElement):

    def __init__(self, *args, **kwargs):
        for element in self._get_page_elements():
            if isinstance(element, (WebElement, MobileElement)):
                # If element is not a page object, update element parent
                element.parent = self
        super(Group, self).__init__(*args, **kwargs)


    def _get_page_elements(self):
        """Return page elements and page objects of this page object

        :returns: list of page elements and page objects
        """
        page_elements = []
        for attribute, value in list(self.__dict__.items()) + list(self.__class__.__dict__.items()):
            breakpoint()
            if attribute != 'parent' and isinstance(value, CoreElement):
                page_elements.append(value)
        return page_elements
