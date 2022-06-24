from dyatel.dyatel_play.play_driver import PlayDriver
from dyatel.dyatel_play.play_page import PlayPage
from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


class Page(WebPage, MobilePage, PlayPage):

    def __init__(self, locator, locator_type=None, name=None):

        self.page_class = self.__get_page_class()
        if self.page_class is PlayPage:
            PlayPage.__init__(self, locator, locator_type, name)
        else:
            super(self.page_class, self).__init__(locator, locator_type, name)

    def __get_page_class(self):
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
