from __future__ import annotations

from typing import Generator, Sequence, TypeVar

T = TypeVar("T")


def marklast(seq: Sequence[T]) -> Generator[tuple[T, bool], None, None]:
    last_idx = len(seq) - 1
    for i, x in enumerate(seq):
        yield x, i == last_idx


def common_prefix(a: str, b: str) -> str:
    buf = ""
    for c1, c2 in zip(a, b):
        if c1 != c2:
            break
        buf += c1
    return buf
