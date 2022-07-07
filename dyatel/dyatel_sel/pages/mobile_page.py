from dyatel.dyatel_sel.core.core_page import CorePage


class MobilePage(CorePage):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of mobile page with appium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        CorePage.__init__(self, locator=locator, locator_type=locator_type, name=name)
