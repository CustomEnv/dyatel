from selenium.webdriver.remote.command import Command


def get_driver_status(driver):
    try:
        driver.execute(Command.STATUS)
        return 'Opened'
    except:
        return 'Closed'


class CoreDriver:
    driver = None

    mobile = False
    is_ios = False
    is_android = False

    def __init__(self, driver):
        self.driver = driver

    # def __getattr__(self, name):
    #     return getattr(self.driver, name)

    def is_driver_opened(self):
        return get_driver_status(self.driver) == 'Opened'

    def is_driver_closed(self):
        return get_driver_status(self.driver) == 'Closed'
