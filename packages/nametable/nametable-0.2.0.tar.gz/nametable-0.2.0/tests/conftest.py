from typing import Optional
from pytest import fixture
from hypothesis.strategies import builds, binary, integers, lists, composite, tuples

from numpy import array, ubyte
from numpy.typing import NDArray


def pattern_meta():
    from nametable.PatternMeta import PatternMeta

    return builds(PatternMeta, binary(min_size=16, max_size=16))


def pattern():
    from nametable.Pattern import Pattern

    return builds(Pattern, pattern_meta())


def animator(min_frame: int = 0, max_frame: Optional[int] = None):
    from nametable.Animator import Animator

    return builds(Animator, integers(min_value=min_frame, max_value=max_frame))


@composite
def pattern_animated_tuple(draw, min_size: int = 0, max_size: Optional[int] = None):
    stack = draw(lists(pattern(), min_size=min_size, max_size=max_size))
    ani = draw(animator(max_frame=len(stack)))
    return stack, ani


@composite
def pattern_animated(draw, min_frames: int = 0, max_frames: Optional[int] = None):
    from nametable.PatternAnimated import PatternAnimated

    stack, animator = draw(pattern_animated_tuple(min_size=min_frames, max_size=max_frames))

    return PatternAnimated(stack, animator)


@composite
def pattern_array(draw, min_size: int = 0, max_size: Optional[int] = None):
    return draw(lists(pattern(), min_size=min_size, max_size=max_size))


@composite
def pattern_table(draw, min_size: int = 0, max_size: Optional[int] = None):
    from nametable.PatternTable import PatternTable

    array = draw(pattern_array(min_size=min_size, max_size=max_size))

    return PatternTable(array)


@composite
def pattern_table_animated_tuple(draw, min_size: int = 0, max_size: Optional[int] = None):
    tables = draw(lists(pattern_table(), min_size=min_size, max_size=max_size))
    ani = draw(animator(max_frame=len(tables)))
    return tables, ani


@composite
def pattern_table_animated(draw, min_frames: int = 0, max_frames: Optional[int] = None):
    from nametable.PatternTableAnimated import PatternTableAnimated

    tables, animator = draw(pattern_table_animated_tuple(min_size=min_frames, max_size=max_frames))

    return PatternTableAnimated(tables, animator)


@composite
def block(draw, min_size: int = 0, max_size: Optional[int] = None):
    from nametable.Block import Block

    table = draw(pattern_table(min_size=min_size, max_size=max_size))
    blocks = draw(
        tuples(
            integers(min_value=0, max_value=len(table.pattern_array)),
            integers(min_value=0, max_value=len(table.pattern_array)),
            integers(min_value=0, max_value=len(table.pattern_array)),
            integers(min_value=0, max_value=len(table.pattern_array)),
        )
    )

    return Block(table, blocks)


@fixture
def _pattern_data():
    def pattern_data_generator():
        yield {
            "data": bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"),
            "numpy": array(
                [
                    [0, 1, 0, 0, 0, 0, 0, 3],
                    [1, 1, 0, 0, 0, 0, 3, 0],
                    [0, 1, 0, 0, 0, 3, 0, 0],
                    [0, 1, 0, 0, 3, 0, 0, 0],
                    [0, 0, 0, 3, 0, 2, 2, 0],
                    [0, 0, 3, 0, 0, 0, 0, 2],
                    [0, 3, 0, 0, 0, 0, 2, 0],
                    [3, 0, 0, 0, 0, 2, 2, 2],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "data": bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")[::-1],
            "numpy": array(
                [
                    [3, 0, 0, 0, 0, 1, 1, 1],
                    [0, 3, 0, 0, 0, 0, 1, 0],
                    [0, 0, 3, 0, 0, 0, 0, 1],
                    [0, 0, 0, 3, 0, 1, 1, 0],
                    [0, 2, 0, 0, 3, 0, 0, 0],
                    [0, 2, 0, 0, 0, 3, 0, 0],
                    [2, 2, 0, 0, 0, 0, 3, 0],
                    [0, 2, 0, 0, 0, 0, 0, 3],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "data": bytes.fromhex("14 2C 44 84 01 02 04 06 10 20 40 80 61 11 22 78"),
            "numpy": array(
                [
                    [0, 0, 0, 3, 0, 1, 0, 0],
                    [0, 0, 3, 0, 1, 1, 0, 0],
                    [0, 3, 0, 0, 0, 1, 0, 0],
                    [3, 0, 0, 0, 0, 1, 0, 0],
                    [0, 2, 2, 0, 0, 0, 0, 3],
                    [0, 0, 0, 2, 0, 0, 1, 2],
                    [0, 0, 2, 0, 0, 1, 2, 0],
                    [0, 2, 2, 2, 2, 1, 1, 0],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "data": bytes.fromhex("14 2C 44 84 01 02 04 06 10 20 40 80 61 11 22 78")[::-1],
            "numpy": array(
                [
                    [0, 1, 1, 1, 1, 2, 2, 0],
                    [0, 0, 1, 0, 0, 2, 1, 0],
                    [0, 0, 0, 1, 0, 0, 2, 1],
                    [0, 1, 1, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 2, 0, 0],
                    [0, 3, 0, 0, 0, 2, 0, 0],
                    [0, 0, 3, 0, 2, 2, 0, 0],
                    [0, 0, 0, 3, 0, 2, 0, 0],
                ],
                dtype=ubyte,
            ),
        }

    return pattern_data_generator()


@fixture(params=[f"Pattern Data {index}" for index in range(4)])
def pattern_data(_pattern_data) -> tuple[tuple[bytes, NDArray[ubyte]], ...]:
    return next(_pattern_data)


@fixture
def _block_data():
    from nametable.PatternMeta import PatternMeta
    from nametable.Pattern import Pattern

    def block_data_generator():
        yield {
            "pattern": Pattern(PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87"))),
            "numpy": array(
                [
                    [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],
                    [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],
                    [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
                    [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],
                    [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],
                    [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],
                    [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],
                    [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],
                    [0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3],
                    [1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0],
                    [0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0],
                    [0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0],
                    [0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0],
                    [0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2],
                    [0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0],
                    [3, 0, 0, 0, 0, 2, 2, 2, 3, 0, 0, 0, 0, 2, 2, 2],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "pattern": Pattern(PatternMeta(bytes.fromhex("41 C2 44 48 10 20 40 80 01 02 04 08 16 21 42 87")[::-1])),
            "numpy": array(
                [
                    [3, 0, 0, 0, 0, 1, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1],
                    [0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0],
                    [0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1],
                    [0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0],
                    [0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0],
                    [0, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0],
                    [2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0],
                    [0, 2, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 1, 1, 1, 3, 0, 0, 0, 0, 1, 1, 1],
                    [0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0],
                    [0, 0, 3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1],
                    [0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0],
                    [0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0],
                    [0, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0],
                    [2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0],
                    [0, 2, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "pattern": Pattern(PatternMeta(bytes.fromhex("14 2C 44 84 01 02 04 06 10 20 40 80 61 11 22 78"))),
            "numpy": array(
                [
                    [0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0],
                    [0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0],
                    [0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0],
                    [3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0],
                    [0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3],
                    [0, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 1, 2],
                    [0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 1, 2, 0],
                    [0, 2, 2, 2, 2, 1, 1, 0, 0, 2, 2, 2, 2, 1, 1, 0],
                    [0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 3, 0, 1, 0, 0],
                    [0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0],
                    [0, 3, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0],
                    [3, 0, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0],
                    [0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3],
                    [0, 0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 1, 2],
                    [0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 1, 2, 0],
                    [0, 2, 2, 2, 2, 1, 1, 0, 0, 2, 2, 2, 2, 1, 1, 0],
                ],
                dtype=ubyte,
            ),
        }
        yield {
            "pattern": Pattern(PatternMeta(bytes.fromhex("14 2C 44 84 01 02 04 06 10 20 40 80 61 11 22 78")[::-1])),
            "numpy": array(
                [
                    [0, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1, 2, 2, 0],
                    [0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 2, 1, 0],
                    [0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 2, 1],
                    [0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0],
                    [0, 3, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0],
                    [0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0],
                    [0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0],
                    [0, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1, 1, 1, 2, 2, 0],
                    [0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 2, 1, 0],
                    [0, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 1, 0, 0, 2, 1],
                    [0, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 0, 0, 0, 0, 3],
                    [3, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 2, 0, 0],
                    [0, 3, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0],
                    [0, 0, 3, 0, 2, 2, 0, 0, 0, 0, 3, 0, 2, 2, 0, 0],
                    [0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0],
                ],
                dtype=ubyte,
            ),
        }

    return block_data_generator()


@fixture(params=[f"Block Data {index}" for index in range(4)])
def block_data(_block_data):
    return next(_block_data)
