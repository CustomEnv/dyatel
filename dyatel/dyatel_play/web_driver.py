class WebDriver:
    driver = None
    context = None

    def __init__(self, driver, initial_page=True):
        self.driver = driver

        if initial_page:
            self.context = self.driver.new_page()

        WebDriver.driver = self.driver
        WebDriver.context = self.context
