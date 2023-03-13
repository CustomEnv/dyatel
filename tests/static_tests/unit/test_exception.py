from dyatel.exceptions import DriverWrapperException


def test_exception():
    try:
        raise DriverWrapperException('1')
    except DriverWrapperException as exc:
        assert exc.__suppress_context__ is True
