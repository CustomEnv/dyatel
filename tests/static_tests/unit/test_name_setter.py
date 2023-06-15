import types

from dyatel.mixins.core_mixin import set_name_for_attr


def test_name_setter_positive():
    obj = types.SimpleNamespace()
    obj.name = ''
    set_name_for_attr()
