from hypothesis import given
from hypothesis.strategies import binary, lists

from numpy import array_equal

from tests.conftest import pattern_meta

from nametable.PatternMeta import PatternMeta


@given(binary(min_size=16, max_size=16))
def test_initialization(bytes):
    PatternMeta(bytes)


@given(pattern_meta(), pattern_meta())
def test_equality(pattern_meta, pattern_meta_):
    assert (pattern_meta == pattern_meta_) == (list(pattern_meta.data) == list(pattern_meta_.data))


@given(pattern_meta(), pattern_meta())
def test_inequality(pattern_meta, pattern_meta_):
    assert (pattern_meta != pattern_meta_) == (list(pattern_meta.data) != list(pattern_meta_.data))


@given(pattern_meta(), pattern_meta())
def test_equality_cannot_be_not_equal(pattern_meta, pattern_meta_):
    assert (pattern_meta == pattern_meta_) != (pattern_meta.data != pattern_meta_.data)


@given(pattern_meta())
def test_conversion(pattern_meta):
    assert pattern_meta == PatternMeta.from_numpy_array(pattern_meta.numpy_array)


@given(lists(pattern_meta()))
def test_hash(pattern_metas):
    d = {}
    for meta in pattern_metas:
        if meta in d:
            assert d[meta] == meta
        d.update({meta: meta})


@given(pattern_meta())
def test_numpy_array_shape(pattern_meta):
    assert pattern_meta.numpy_array.shape == (8, 8)


def test_bytes_conversion(pattern_data):
    assert array_equal(PatternMeta(pattern_data["data"]).numpy_array, pattern_data["numpy"])
