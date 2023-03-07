from dyatel.base.element import Element


class Section(Element):
    def __init__(self):
        self.iel = Element('iel', name='iel', parent=self)
        super().__init__('section', name='Section')

    oiel = Element('oiel', name='oiel')


def test_promote_parent_element_recursion(mocked_selenium_driver):
    section = Section()
    section.oiel.parent = None
    section.iel.parent = None
