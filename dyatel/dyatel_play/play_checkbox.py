from __future__ import annotations

from playwright.sync_api import Locator


class PlayCheckbox:

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False, **kwargs):
        """
        Initializing of checkbox with playwright driver

        :param locator: checkbox locator. Can be defined without locator_type
        :param locator_type: compatibility arg - specific locator type
        :param name: name of checkbox (will be attached to logs)
        :param parent: parent of checkbox. Can be Web/MobileElement, Web/MobilePage or Group objects etc.
        :param wait: add element waiting in `wait_page_loaded` function of PlayPage
        :param by_attr: compatibility arg - does nothing
        """
        from dyatel.dyatel_play.play_element import PlayElement
        self.wrapped_element = PlayElement(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    @property
    def element(self) -> Locator:
        """
        Get playwright Locator object

        :return: playwright WebElement
        """
        return self.wrapped_element.element

    def is_checked(self) -> bool:
        """
        Is checkbox checked

        :return: bool
        """
        return self.element.is_checked()

    def check(self) -> PlayCheckbox:
        """
        Check current checkbox

        :return: self
        """
        self.element.check()

        return self

    def uncheck(self) -> PlayCheckbox:
        """
        Uncheck current checkbox

        :return: self
        """
        self.element.uncheck()

        return self

    @property
    def get_text(self) -> str:
        """
        Get text of current checkbox

        :return: checkbox text
        """
        return self.element.text_content() if self.element.text_content() else self.element.input_value()
