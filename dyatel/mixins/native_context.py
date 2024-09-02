from dyatel.mixins.objects.locator import *


class NativeContext:

    def __init__(self, driver_wrapper):
        self.driver_wrapper = driver_wrapper

    def __enter__(self):
        self.driver_wrapper.switch_to_native()

    def __exit__(self, *args):
        self.driver_wrapper.switch_to_web()


class NativeSafari:

    def __init__(self, driver_wrapper):
        self.driver_wrapper = driver_wrapper

        from dyatel.base.element import Element

        top_bar_locator = ios_mobile_top_bar_locator
        if driver_wrapper.is_tablet:
            top_bar_locator = ios_tablet_top_bar_locator

        self.top_bar = Element(Locator(top_bar_locator, tablet=ios_tablet_top_bar_locator), name='safari top bar',
                               driver_wrapper=driver_wrapper)
        self.bottom_bar = Element(ios_mobile_small_bottom_bar_locator, name='safari bottom bar',
                                  driver_wrapper=driver_wrapper)
        self.keyboard_done_button = Element(locator=ios_keyboard_hide_button, name='keyboard Done button',
                                            driver_wrapper=driver_wrapper)

    def get_bottom_bar_height(self) -> int:
        """
        Get iOS/iPadOS bottom bar height

        :return: int
        """
        if self.driver_wrapper.is_tablet:
            return 0  # iPad does not have bottom bar

        bottom_bar_height = self.bottom_bar.size.height
        if bottom_bar_height > 350:  # Large devices have different locator
            self.bottom_bar.locator = ios_mobile_large_bottom_bar_locator
            bottom_bar_height = self.bottom_bar.size.height

        return bottom_bar_height
