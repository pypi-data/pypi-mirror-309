from hypothesis import given

from nametable.Pattern import Pattern

from tests.conftest import pattern_meta, pattern


@given(pattern_meta())
def test_initialization(pattern_meta):
    Pattern(pattern_meta)


@given(pattern_meta())
def test_one_copy_for_equality(pattern_meta):
    Pattern._patterns.clear()

    assert Pattern(pattern_meta) is Pattern(pattern_meta)


@given(pattern())
def test_conversion(pattern):
    assert pattern == Pattern.from_numpy_array(pattern.numpy_array)


@given(pattern())
def test_numpy_array_shape(pattern):
    assert pattern.numpy_array.shape == (8, 8)
