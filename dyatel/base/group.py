from dyatel.base.element import Element
from dyatel.internal_utils import get_child_elements


class AfterInitMeta(type):
    """ Call a custom function right after __init__ of original class """

    def __call__(cls, *args, **kwargs):
        """
        Wrapper for calling a custom function right after __init__ of original class

        :param args: original class args
        :param kwargs: original class kwargs
        :return: class object
        """
        obj = type.__call__(cls, *args, **kwargs)
        obj.after_init()
        return obj


class Group(Element, metaclass=AfterInitMeta):
    """ Group of elements. Should be defined as class """

    def __init__(self, locator: str, locator_type='', name=''):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of group (will be attached to logs)
        """
        Element.__init__(self, locator, locator_type, name)

    def after_init(self):
        """
        Initializing of Group class variables, if their instance os Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        for element in get_child_elements(self, Element):
            element.parent = self
