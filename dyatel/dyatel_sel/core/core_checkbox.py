from __future__ import annotations


class CoreCheckbox:

    def __init__(self, locator: str, locator_type='', name='', parent=None, wait=False, by_attr=False):
        """
        Initializing of core checkbox with appium/selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects etc.
        :param wait: add element waiting in `wait_page_loaded` function of CorePage
        :param by_attr: get is_checked state by custom attribute
        """
        from dyatel.dyatel_sel.elements.web_element import CoreElement
        self.wrapped_element = CoreElement(locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)
        self.checked = None
        self.by_attr = by_attr

    @property
    def element(self):
        """
        Get selenium WebElement object

        :return: selenium WebElement
        """
        return self.wrapped_element.element

    def is_checked(self):
        """
        Is checkbox checked

        :return: bool
        """
        is_checked_selenium = self.element.is_selected()
        return self.checked if self.by_attr else is_checked_selenium

    def check(self):
        """
        Check current checkbox

        :return: self
        """
        if not self.is_checked():
            self.element.click()
            self.checked = True

        return self

    def uncheck(self):
        """
        Uncheck current checkbox

        :return: self
        """
        if self.is_checked():
            self.element.click()
            self.checked = False

        return self

    @property
    def get_text(self):
        """
        Get text of current checkbox

        :return: checkbox text
        """
        return self.element.text if self.element.text else self.element.get_attribute('value')
