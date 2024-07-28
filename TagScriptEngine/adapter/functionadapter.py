from __future__ import annotations

from typing import Callable, Tuple

from ..interface import Adapter
from ..verb import Verb


__all__: Tuple[str, ...] = ("FunctionAdapter",)


class FunctionAdapter(Adapter):
    __slots__: Tuple[str, ...] = ("fn",)

    def __init__(self, function_pointer: Callable[[], str]) -> None:
        self.fn = function_pointer
        super().__init__()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} fn={self.fn!r}>"

    def get_value(self, ctx: Verb) -> str:  # type: ignore
        return str(self.fn())
