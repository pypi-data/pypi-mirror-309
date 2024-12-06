from __future__ import annotations

from dataclasses import dataclass
from typing import Generator

from .base import ToxBase


@dataclass(frozen=True)
class ToxOptions(ToxBase):
    """
    A "generative" piece of a tox env name.

    These work differently than shell expansion, and notably can't be nested.
    Whitespace is ignored when parsing, but always output without it.

    e.g. `{a , b }` -> `{a,b}`

    Note that `options` should never be an empty tuple, even when parsing `{}`
    it should be `("",)` -- one item, which is empty string.
    """

    options: tuple[str, ...]

    def __iter__(self) -> Generator[str, None, None]:
        assert self.options
        yield from self.options

    def addprefix(self, prefix: str) -> "ToxOptions":
        return self.__class__(tuple(prefix + x for x in self.options))

    def removeprefix(self, prefix: str) -> "ToxOptions":
        assert self.startswith(prefix)
        return self.__class__(tuple(x[len(prefix) :] for x in self.options))

    def addsuffix(self, suffix: str) -> "ToxOptions":
        return self.__class__(tuple(x + suffix for x in self.options))

    def removesuffix(self, suffix: str) -> "ToxOptions":
        assert self.endswith(suffix)
        return self.__class__(tuple(x[: -len(suffix)] for x in self.options))

    @classmethod
    def parse(cls, s: str) -> "ToxOptions":
        assert s[0] == "{"
        assert s[-1] == "}"
        return cls(tuple(i.strip() for i in s[1:-1].split(",")))

    def __str__(self) -> str:
        return "{%s}" % ",".join(self.options)
