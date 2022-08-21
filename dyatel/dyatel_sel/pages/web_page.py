from dyatel.dyatel_sel.core.core_page import CorePage
from dyatel.dyatel_sel.sel_utils import get_locator_type


class WebPage(CorePage):

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of web page with selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        self.locator_type = locator_type if locator_type else get_locator_type(locator)
        super().__init__(locator=locator, locator_type=locator_type, name=name)
