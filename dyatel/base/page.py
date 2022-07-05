from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


class Page(WebPage, MobilePage, PlayPage):
    """ Page object crossroad. Should be defined as class """

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of page based on current driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self.page_class = self.__get_page_class()
        self.page_class.__init__(self, locator, locator_type, name)

    def __get_page_class(self):
        """
        Get page class in according to current driver, and set him as base class

        :return: page class
        """
        if PlayDriver.driver:
            Page.__bases__ = PlayPage,
            return PlayPage
        elif CoreDriver.driver and CoreDriver.mobile:
            Page.__bases__ = MobilePage,
            return MobilePage
        elif CoreDriver.driver and not CoreDriver.mobile:
            Page.__bases__ = WebPage,
            return WebPage
        else:
            raise Exception('Cant specify Page')
