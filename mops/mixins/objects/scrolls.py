# TODO: next_version - inherit from Enum
class ScrollTo:
    START = 'start'
    CENTER = 'center'
    END = 'end'
    NEAREST = 'nearest'


# TODO: next_version - inherit from Enum
class ScrollTypes:
    SMOOTH = 'smooth'
    INSTANT = 'instant'


scroll_into_view_blocks = (ScrollTo.START, ScrollTo.CENTER, ScrollTo.END, ScrollTo.NEAREST)
