from hypothesis import given

from nametable.PatternTableAnimated import PatternTableAnimated

from tests.conftest import pattern_table_animated, pattern_table_animated_tuple


@given(pattern_table_animated_tuple())
def test_initialization(data):
    pattern_tables, animator = data
    PatternTableAnimated(pattern_tables, animator)


@given(pattern_table_animated())
def test_animation(pattern_table_animated):
    for frame in range(len(pattern_table_animated.pattern_tables)):
        pattern_table_animated.animator.frame = frame
        assert pattern_table_animated.pattern_array == pattern_table_animated.pattern_tables[frame].pattern_array
