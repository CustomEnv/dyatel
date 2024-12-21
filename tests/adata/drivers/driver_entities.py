class DriverEntities:

    def __init__(
            self,
            request,
            driver_name,
            platform,
            selenium_chrome_options,
            selenium_firefox_options,
            env: str,
            **kwargs, # noqa
    ):
        self.request = request
        self.driver_name = driver_name
        self.platform = platform
        self.selenium_chrome_options = selenium_chrome_options
        self.selenium_firefox_options = selenium_firefox_options
        self.config = self.request.config
        self.env = env
