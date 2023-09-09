from typing import Optional


class DriverWrapperException(Exception):
    """
    Base driver wrapper exceptions
    """

    def __init__(self, msg: Optional[str] = None):
        self.msg = msg
        self.__suppress_context__ = True

    def __str__(self) -> str:
        return f"Message: {self.msg}"


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


class NoSuchParentException(DriverWrapperException):
    """
    Thrown when parent could not be found
    """
    pass


class ElementNotInteractableException(DriverWrapperException):
    """
    Thrown when element found and enabled but not interactable
    """
    pass


class UnsuitableArgumentsException(DriverWrapperException):
    """
    Thrown when object initialised with unsuitable arguments
    """
    pass


class NotInitializedException(DriverWrapperException):
    """
    Thrown when getting access to not initialized object
    """
    pass
