from typing import Any

from dyatel.base.element import Element
from dyatel.internal_utils import get_child_elements, get_object_args


class AfterInitMeta(type):
    """ Call a custom function right after __init__ of original class """

    def __call__(cls, *args, **kwargs):
        """
        Wrapper for calling a custom function right after __init__ of original class

        :param args: original class args
        :param kwargs: original class kwargs
        :return: class object
        """
        #  FIXME: required when Group defined without __init__
        try:
            obj = type.__call__(cls, *args, **kwargs)
        except AttributeError:
            obj = type.__call__(cls, **get_object_args(cls))
        obj.set_parent_for_children()
        return obj


class Group(Element, metaclass=AfterInitMeta):
    """ Group of elements. Should be defined as class """

    def __init__(self, locator: str, locator_type='', name='', parent: Any = None, wait=False):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        """
        Element.__init__(self, locator=locator, locator_type=locator_type, name=name, parent=parent, wait=wait)

    def set_parent_for_children(self):
        """
        Initializing of Group class variables, if their instance os Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        for element in get_child_elements(self, Element):
            element.parent = self
