from __future__ import annotations

from typing import Optional, Tuple, cast

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("SubstringBlock",)


class SubstringBlock(verb_required_block(True, parameter=True)):  # type: ignore
    ACCEPTED_NAMES: Tuple[str, ...] = ("substr", "substring")

    def process(self, ctx: Context) -> Optional[str]:
        try:
            if "-" not in cast(str, ctx.verb.parameter):
                return cast(str, ctx.verb.payload)[int(float(cast(str, ctx.verb.parameter))) :]

            spl = cast(str, ctx.verb.parameter).split("-")
            start = int(float(spl[0]))
            end = int(float(spl[1]))
            return cast(str, ctx.verb.payload)[start:end]
        except Exception:
            return
