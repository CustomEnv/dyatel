from selenium_master.core.core_driver import CoreDriver
from selenium_master.pages.mobile_page import MobilePage
from selenium_master.pages.web_page import WebPage


class BasePage(MobilePage, WebPage):
    def __init__(self, *args, **kwargs):
        # if os.environ.get('mobile', default=False):
        if CoreDriver.mobile:
            self.root_page_class = MobilePage
            super(MobilePage, self).__init__(*args, **kwargs)
        else:
            self.root_page_class = WebPage
            super(WebPage, self).__init__(*args, **kwargs)
