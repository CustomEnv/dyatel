from mops.visual_comparison import VisualComparison


def test_remove_unexpected_underscores():
    assert VisualComparison._remove_unexpected_underscores('__test_1__2___3____4') == '_test_1_2_3_4'
