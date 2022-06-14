import os

from selenium_master.pages.mobile_page import MobilePage
from selenium_master.pages.web_page import WebPage


class BasePage(MobilePage, WebPage):
    def __init__(self, *args, **kwargs):
        if os.environ.get('mobile', default=False):
            super(MobilePage, self).__init__(*args, **kwargs)
        else:
            super(WebPage, self).__init__(*args, **kwargs)
