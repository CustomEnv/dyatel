from logging import info

from playwright.sync_api import Page as PlayPage
from playwright.sync_api import Browser


class PlayDriver:
    driver: Browser = None
    context: PlayPage = None

    def __init__(self, driver, initial_page=True):
        self.driver: Browser = driver

        if initial_page and not self.driver.contexts:
            self.context: PlayPage = self.driver.new_page()

        PlayDriver.driver = self.driver
        PlayDriver.context = self.context

    def get(self, url):
        info(f'Navigating to url {url}')
        self.context.goto(url)

    def is_driver_opened(self):
        return self.driver.is_connected()

    def is_driver_closed(self):
        return not self.driver.is_connected()
