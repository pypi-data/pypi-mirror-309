""" test ae.kivy_relief_canvas portion.

help/hints to make unit tests for
kivy widgets working on gitlab-CI
would be highly appreciated.
"""
from ae.kivy_relief_canvas import relief_colors, ReliefCanvas


def test_declaration():
    assert ReliefCanvas


class TestHelpers:
    def test_relief_colors_default_args(self):
        assert relief_colors() == ([0.6, 0.6, 0.6], [0.3, 0.3, 0.3])

        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5]) == ([0.6, 0.6, 0.6], [0.3, 0.3, 0.3])
        assert relief_colors(color_or_ink=(0.5, 0.5, 0.5)) == ([0.6, 0.6, 0.6], [0.3, 0.3, 0.3])

        assert relief_colors(color_or_ink=[1.0, 0.5, 0.5]) == ([0.6, 0.3, 0.3], [0.3, 0.15, 0.15])
        assert relief_colors(color_or_ink=(1.0, 0.5, 0.5)) == ([0.6, 0.3, 0.3], [0.3, 0.15, 0.15])

        assert relief_colors(darken_factors=(0.3, 0.6)) == ([0.3, 0.3, 0.3], [0.6, 0.6, 0.6])

    def test_relief_colors_auto_hide(self):
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0.1]) == ([0.6, 0.6, 0.6], [0.3, 0.3, 0.3])
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0.0]) == ()
        assert relief_colors(color_or_ink=[0.5, 0.5, 0.5, 0]) == ()
