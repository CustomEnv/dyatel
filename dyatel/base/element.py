from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement


class Element(WebElement, MobileElement, PlayElement):

    def __init__(self, locator, locator_type=None, name=None, parent=None):
        self.driver = None
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent

        self.element_class = self.__get_element_class()
        if self.element_class:
            self.element_class.__init__(self, locator, locator_type=locator_type, name=name, parent=parent)

    def __get_element_class(self):
        if PlayDriver.driver:
            Element.__bases__ = PlayElement,
            return PlayElement
        elif CoreDriver.driver and CoreDriver.mobile:
            Element.__bases__ = MobileElement,
            return MobileElement
        elif CoreDriver.driver and not CoreDriver.mobile:
            Element.__bases__ = WebElement,
            return WebElement
