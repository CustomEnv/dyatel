from dyatel.utils.internal_utils import check_kwargs, available_kwarg_keys


def test_check_kwargs_negative():
    try:
        check_kwargs({'tester': None})
    except AssertionError:
        pass
    else:
        raise Exception('Unexpected behaviour')


def test_check_kwargs_positive():
    check_kwargs(dict(zip(available_kwarg_keys, range(len(available_kwarg_keys)))))
