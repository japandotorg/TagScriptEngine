from __future__ import annotations

from typing import Optional, Tuple, cast

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("CountBlock", "LengthBlock")


class CountBlock(verb_required_block(True, payload=True)):  # type: ignore
    """
    The count block will count how much of text is in message.
    This is case sensitive and will include substrings, if you
    don't provide a parameter, it will count the spaces in the
    message.

    **Usage:** ``{count([text]):<message>}``

    **Aliases:** ``None``

    **Payload:** ``message``

    **Parameter:** text

    .. tagscript::
        {count(Tag):TagScriptEngine}
        # 1

        {count(Tag): Tag Script Engine TagScriptEngine}
        # 2
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("count",)

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.parameter:
            payload: str = cast(str, ctx.verb.payload)
            return str(payload.count(ctx.verb.parameter))
        return str(len(cast(str, ctx.verb.payload)) + 1)


class LengthBlock(verb_required_block(True, payload=True)):  # type: ignore
    """
    The length block will check the length of the given String.
    If a parameter is passed in, the block will check the length
    based on what you passed in, w for word, s for spaces.
    If you provide an invalid parameter, the block will return -1.

    **Usage:** ``{length(<text>)}``

    **Aliases:** ``len``

    **Payload:** None

    **Parameter:** ``text``

    .. tagscript::

        {len("TagScriptEngine")}
        15
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("length", "len")

    def process(self, ctx: Context) -> Optional[str]:
        return str(len(ctx.verb.parameter)) if ctx.verb.parameter else "-1"
