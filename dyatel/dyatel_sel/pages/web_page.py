from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver

from dyatel.dyatel_sel.core.core_driver import CoreDriver
from dyatel.dyatel_sel.core.core_page import CorePage


class WebPage(CorePage):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of web page with selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self.driver: SeleniumWebDriver = CoreDriver.driver
        CorePage.__init__(self, locator=locator, locator_type=locator_type, name=name)
