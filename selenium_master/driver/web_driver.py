from selenium.webdriver.remote.command import Command

from selenium_master.driver.core_driver import CoreDriver


def get_driver_status(driver):
    try:
        driver.execute(Command.STATUS)
        return 'Opened'
    except:
        return 'Closed'


class WebDriver(CoreDriver):
    mobile = False

    def __init__(self, driver):
        self.driver = driver
        super(WebDriver, self).__init__(driver=self.driver)
        CoreDriver.driver = self.driver

    def is_driver_opened(self):
        return get_driver_status(self.driver) == 'Opened'

    def is_driver_closed(self):
        return get_driver_status(self.driver) == 'Closed'
