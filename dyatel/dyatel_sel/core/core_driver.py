from typing import Union
from logging import info

from appium.webdriver.webdriver import WebDriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.command import Command


def get_driver_status(driver):
    try:
        driver.execute(Command.STATUS)
        return 'Opened'
    except:
        return 'Closed'


class CoreDriver:
    driver: Union[AppiumDriver, SeleniumWebDriver] = None

    mobile = False
    desktop = False
    is_ios = False
    is_android = False

    def __init__(self, driver: Union[AppiumDriver, SeleniumWebDriver]):
        self.driver: Union[AppiumDriver, SeleniumWebDriver] = driver

    def is_driver_opened(self):
        return get_driver_status(self.driver) == 'Opened'

    def is_driver_closed(self):
        return get_driver_status(self.driver) == 'Closed'

    def get(self, url):
        info(f'Navigating to url {url}')
        return self.driver.get(url)
