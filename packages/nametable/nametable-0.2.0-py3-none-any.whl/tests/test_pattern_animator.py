from hypothesis import given

from nametable.PatternAnimated import PatternAnimated

from tests.conftest import pattern_animated, pattern_animated_tuple


@given(pattern_animated_tuple())
def test_initialization(data):
    pattern_stack, animator = data
    PatternAnimated(pattern_stack, animator)


@given(pattern_animated())
def test_animation(pattern_animated):
    for frame in range(len(pattern_animated.stack)):
        pattern_animated.animator.frame = frame
        assert pattern_animated.meta == pattern_animated.stack[frame].meta


@given(pattern_animated())
def test_numpy_array_shape(pattern_animated):
    for frame in range(len(pattern_animated.stack)):
        pattern_animated.animator.frame = frame
        assert pattern_animated.numpy_array.shape == (8, 8)
