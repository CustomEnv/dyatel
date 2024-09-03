import time
from typing import Union

import pytest

from dyatel.exceptions import TimeoutException
from dyatel.utils.internal_utils import wait_condition, WAIT_METHODS_DELAY
from dyatel.utils.logs import autolog
from dyatel.mixins.objects.wait_result import Result


namespace_default_cals_count = 3


class MockNamespace:

    def __init__(self, log_msg: str, call_count: int):
        self.call_count = call_count
        self.actual_call_count = 0
        self.log_msg = log_msg

    def log(self, *args, **kwargs):
        return autolog(*args, **kwargs)

    def get_result(self):
        if self.actual_call_count == self.call_count:
            return True

        self.actual_call_count += 1

        return False

    @wait_condition
    def wait_something(self, timeout: Union[int, float] = 1) -> bool:
        return Result(  # noqa
            execution_result=self.get_result(),
            log=self.log_msg,
            exc=TimeoutException('wait some condition failed!', timeout=timeout),
        )


@pytest.mark.parametrize('call_count', [0, 3], ids=['initial pass', 'pass after 3 retries'])
def test_wait_condition_positive(caplog, call_count):
    namespace = MockNamespace('wait some condition', call_count=call_count)
    start_time = time.time()
    result = namespace.wait_something()
    execution_time = time.time() - start_time
    assert execution_time < WAIT_METHODS_DELAY * call_count or 1, \
        'delay inside wait_condition decorator unexpectedly executed for initially passed wait'
    assert result == namespace, 'wait condition method does not return the `self` object'
    assert caplog.messages.count(namespace.log_msg) == 1, 'log message throttled'


def test_wait_condition_negative_with_wait(caplog):
    call_count = 5
    timeout = call_count / 110
    namespace = MockNamespace('wait some condition', call_count=call_count)
    start_time = time.time()

    try:
        namespace.wait_something(timeout=timeout)
    except TimeoutException as exc:
        assert exc.msg == f'wait some condition failed! after {timeout} seconds.'
    else:
        raise Exception('Unexpected behaviour')

    execution_time = time.time() - start_time

    assert timeout < WAIT_METHODS_DELAY * call_count, 'negative case not covered'
    assert execution_time < WAIT_METHODS_DELAY * call_count,\
        'wait_something execution time for negative check somehow higher that given timeout'
    assert caplog.messages.count(namespace.log_msg) == 1, 'log message throttled'
