import pytest


@pytest.fixture(autouse=True)
def teardown(base_teardown):
    pass
