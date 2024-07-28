from __future__ import annotations

from typing import Tuple
from inspect import ismethod

from ..interface import Adapter
from ..verb import Verb


__all__: Tuple[str, ...] = ("SafeObjectAdapter",)


class SafeObjectAdapter(Adapter):
    __slots__: Tuple[str, ...] = ("object",)

    def __init__(self, base) -> None:
        self.object = base

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} object={repr(self.object)}>"

    def get_value(self, ctx: Verb) -> str:
        if ctx.parameter is None:
            return str(self.object)
        if ctx.parameter.startswith("_") or "." in ctx.parameter:
            return  # type: ignore
        try:
            attribute = getattr(self.object, ctx.parameter)
        except AttributeError:
            return  # type: ignore
        if ismethod(attribute):
            return  # type: ignore
        if isinstance(attribute, float):
            attribute = int(attribute)
        return str(attribute)
