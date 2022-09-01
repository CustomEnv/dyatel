from typing import Optional, Sequence


class DriverWrapperException(Exception):
    """
    Base driver wrapper exceptions
    """

    def __init__(self, msg: Optional[str] = None, screen: Optional[str] = None,
                 stacktrace: Optional[Sequence[str]] = None) -> None:
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self) -> str:
        exception_msg = "Message: %s\n" % self.msg
        if self.screen:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class UnexpectedElementsCountException(DriverWrapperException):
    """
    Thrown when elements count isn't equal to expected
    """
    pass


class UnexpectedValueException(DriverWrapperException):
    """
    Thrown when element contains incorrect value
    """
    pass


class UnexpectedTextException(DriverWrapperException):
    """
    Thrown when element contains incorrect text
    """
    pass


class TimeoutException(DriverWrapperException):
    """
    Thrown when timeout exceeded
    """
    pass


class InvalidSelectorException(DriverWrapperException):
    """
    Thrown when element have invalid selector
    """
    pass


class NoSuchElementException(DriverWrapperException):
    """
    Thrown when element could not be found
    """
    pass
