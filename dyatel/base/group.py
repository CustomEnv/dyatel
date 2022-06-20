from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement


class Group(WebElement, MobileElement):

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        for element in self.child_elements:
            element.parent = self
