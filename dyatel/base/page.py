from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage


class Page(MobilePage, WebPage):
    def __init__(self, *args, **kwargs):
        if CoreDriver.mobile:
            self.root_page_class = MobilePage
            super(MobilePage, self).__init__(*args, **kwargs)
        else:
            self.root_page_class = WebPage
            super(WebPage, self).__init__(*args, **kwargs)
