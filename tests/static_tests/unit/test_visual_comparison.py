from dyatel.visual_comparison import VisualComparison


visual_comparison = VisualComparison(None, None)


def test_remove_unexpected_underscores():
    assert visual_comparison._remove_unexpected_underscores('__test_1__2___3____4') == '_test_1_2_3_4'
