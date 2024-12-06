from hypothesis import given

from nametable.PatternTable import PatternTable

from tests.conftest import pattern_array


@given(pattern_array())
def test_initialization(pattern_array):
    PatternTable(pattern_array)
