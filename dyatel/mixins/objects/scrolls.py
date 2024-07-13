class ScrollTo:
    START = 'start'
    CENTER = 'center'
    END = 'end'
    NEAREST = 'nearest'


class ScrollTypes:
    SMOOTH = 'smooth'
    INSTANT = 'instant'


scroll_into_view_blocks = (ScrollTo.START, ScrollTo.CENTER, ScrollTo.END, ScrollTo.NEAREST)
