from dyatel.dyatel_sel.core.core_driver import CoreDriver


class WebDriver(CoreDriver):

    def __init__(self, driver):
        self.web_driver = driver
        CoreDriver.driver = self.web_driver
        CoreDriver.mobile = False
        super(WebDriver, self).__init__(driver=self.web_driver)
