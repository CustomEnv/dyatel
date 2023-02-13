import pytest

from dyatel.base.driver_wrapper import DriverWrapper


@pytest.fixture(autouse=True)
def teardown(base_teardown):
    yield
    DriverWrapper.is_multiplatform = False
