from hypothesis import given
from hypothesis.strategies import lists

from nametable.Nametable import Nametable

from tests.conftest import block


@given(lists(block()))
def test_initialization(blocks):
    Nametable(blocks)
