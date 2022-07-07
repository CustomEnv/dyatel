from typing import Union, Any

from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_play.play_element import PlayElement
from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement


class Element(WebElement, MobileElement, PlayElement):
    """ Element object crossroad. Should be defined as Page/Group class variable """

    def __init__(self, locator: str, locator_type='', name='', parent: Any = None, wait=False):
        """
        Initializing of element based on current driver
        Skip init if there are no driver, so will be initialized in Page/Group

        :param locator: locator of element. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait
        self._initialized = False

        self.element_class = self.__get_element_class()
        if self.element_class:
            self.element_class.__init__(
                self, locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait
            )

    def __get_element_class(self):
        """
        Get element class in according to current driver, and set him as base class

        :return: element class
        """
        if PlayDriver.driver:
            Element.__bases__ = PlayElement,
            return PlayElement
        elif CoreDriver.driver and CoreDriver.mobile:
            Element.__bases__ = MobileElement,
            return MobileElement
        elif CoreDriver.driver and not CoreDriver.mobile:
            Element.__bases__ = WebElement,
            return WebElement
