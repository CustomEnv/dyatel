from playwright_master.web_element import WebElement


class MixinPlaywright:

    @property
    def cross_button(self):
        return WebElement('[data-qa-marker = cross-button]', name='cross button')
