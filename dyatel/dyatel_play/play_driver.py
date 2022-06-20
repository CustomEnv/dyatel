from logging import info

from playwright.sync_api import Page as PlayPage


class PlayDriver:
    driver = None
    context = None

    def __init__(self, driver, initial_page=True):
        self.driver = driver

        if initial_page and not self.driver.contexts:
            self.context: PlayPage = self.driver.new_page()

        PlayDriver.driver = self.driver
        PlayDriver.context = self.context

    def get(self, url):
        info(f'Navigating to url {url}')
        self.context.goto(url)
