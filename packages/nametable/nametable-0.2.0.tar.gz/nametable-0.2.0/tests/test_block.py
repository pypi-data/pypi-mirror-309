from hypothesis import given
from pytest import raises

from numpy import array_equal

from tests.conftest import pattern_table

from nametable.Block import Block, BlockInvalidSizeException, PatternTableIndexException
from nametable.PatternTable import PatternTable


@given(pattern_table())
def test_only_four_patterns(pattern_table):
    with raises(BlockInvalidSizeException):
        Block(pattern_table, (0, 0, 0, 0, 0))


@given(pattern_table())
def test_bad_reference_to_pattern_table(pattern_table):
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, 0, 0, len(pattern_table.pattern_array) + 1))
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, 0, len(pattern_table.pattern_array) + 1, 0))
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, len(pattern_table.pattern_array) + 1, 0, 0))
    with raises(PatternTableIndexException):
        Block(pattern_table, (len(pattern_table.pattern_array) + 1, 0, 0, 0))


@given(pattern_table())
def test_negative_reference_to_pattern_table(pattern_table):
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, 0, 0, -1))
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, 0, -1, 0))
    with raises(PatternTableIndexException):
        Block(pattern_table, (0, -1, 0, 0))
    with raises(PatternTableIndexException):
        Block(pattern_table, (-1, 0, 0, 0))


def test_bytes_conversion(block_data):
    assert array_equal(Block(PatternTable((block_data["pattern"],)), (0, 0, 0, 0)).numpy_array, block_data["numpy"])
