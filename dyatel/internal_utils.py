def get_child_elements(self, instance):
    """Return page elements and page objects of this page object

    :returns: list of page elements and page objects
    """
    elements = []

    class_items = list(self.__dict__.items()) + list(self.__class__.__dict__.items())

    for parent_class in self.__class__.__bases__:
        class_items += list(parent_class.__dict__.items()) + list(parent_class.__class__.__dict__.items())

    for attribute, value in class_items:
        if isinstance(value, instance):
            elements.append(value)
    return set(elements)


class AfterInitMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.after_init()
        return obj


class Mixin:
    parent = None
    locator = None
    locator_type = None

    def _get_element_logging_data(self):
        parent = self.parent
        current_data = f'Selector: ["{self.locator_type}": "{self.locator}"]'
        if parent:
            parent_data = f'Parent selector: ["{parent.locator_type}": "{parent.locator}"]'
            current_data = f'{current_data}. {parent_data}'
        return current_data
