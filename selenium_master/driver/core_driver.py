class CoreDriver:
    driver = None

    mobile = False
    is_ios = False
    is_android = False

    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, name):
        return getattr(self.driver, name)
