from dyatel.base.element import Element


replaced_data = [1, 2, 3]
value = replaced_data[:1]


class A(Element):

    @property
    def value(self):
        return value

    @property
    def all_elements(self):
        return replaced_data


class B(A):
    pass


def test_overwriting_from_subclass(mocked_selenium_driver):
    obj = B('')
    assert obj.value == value
    assert obj.all_elements == replaced_data


def test_overwriting_from_class(mocked_selenium_driver):
    obj = A('')
    assert obj.value == value
    assert obj.all_elements == replaced_data
