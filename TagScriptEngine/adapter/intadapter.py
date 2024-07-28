from __future__ import annotations

from typing import Tuple

from ..interface import Adapter
from ..verb import Verb


__all__: Tuple[str, ...] = ("IntAdapter",)


class IntAdapter(Adapter):
    __slots__: Tuple[str, ...] = ("integer",)

    def __init__(self, integer: int) -> None:
        self.integer: int = int(integer)

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} integer={repr(self.integer)}>"

    def get_value(self, ctx: Verb) -> str:  # type: ignore
        return str(self.integer)
