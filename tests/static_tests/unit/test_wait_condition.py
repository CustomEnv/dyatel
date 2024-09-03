import time

from dyatel.exceptions import TimeoutException
from dyatel.utils.internal_utils import wait_condition, WAIT_METHODS_DELAY
from dyatel.utils.logs import autolog
from dyatel.mixins.objects.wait_result import Result


namespace_default_cals_count = 3


class MockNamespace:

    def __init__(self, log_msg: str, call_count=namespace_default_cals_count):
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
    def wait_something(self, timeout=1) -> bool:
        return Result(  # noqa
            execution_result=self.get_result(),
            log=self.log_msg,
            exc=TimeoutException('wait some condition failed!', timeout=timeout),
        )


def test_wait_condition_positive_without_wait(caplog):
    namespace = MockNamespace('wait some condition', call_count=0)
    start_time = time.time()
    result = namespace.wait_something()
    execution_time = time.time() - start_time
    assert execution_time < WAIT_METHODS_DELAY, 'wait_condition delay unexpectedly executed for initially passed wait'
    assert result == namespace, 'wait condition method does not return the `self` object'
    assert caplog.messages.count(namespace.log_msg) == 1, 'log message throttled'


def test_wait_condition_positive_with_wait(caplog):
    namespace = MockNamespace('wait some condition', call_count=namespace_default_cals_count)
    start_time = time.time()
    result = namespace.wait_something()
    execution_time = time.time() - start_time
    assert execution_time > WAIT_METHODS_DELAY * namespace_default_cals_count,\
        'wait_condition delay unexpectedly executed for initially passed wait'
    assert result == namespace, 'wait condition method does not return the `self` object'
    assert caplog.messages.count(namespace.log_msg) == 1, 'log message throttled'
