from mops.mixins.internal_mixin import InternalMixin, available_kwarg_keys


def test_check_kwargs_negative():
    try:
        InternalMixin._check_kwargs({'tester': None})
    except AssertionError:
        pass
    else:
        raise Exception('Unexpected behaviour')


def test_check_kwargs_positive():
    InternalMixin._check_kwargs(dict(zip(available_kwarg_keys, range(len(available_kwarg_keys)))))
