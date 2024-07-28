from __future__ import annotations

from typing import Optional, Tuple, cast

from ..exceptions import StopError
from ..interface import verb_required_block
from ..interpreter import Context
from . import helper_parse_if


__all__: Tuple[str, ...] = ("StopBlock",)


class StopBlock(verb_required_block(True, parameter=True)):  # type: ignore
    """
    The stop block stops tag processing if the given parameter is true.
    If a message is passed to the payload it will return that message.

    **Usage:** ``{stop(<bool>):[string]}``

    **Aliases:** ``halt, error``

    **Payload:** string, None

    **Parameter:** bool

    **Example:** ::

        {stop({args}==):You must provide arguments for this tag.}
        # enforces providing arguments for a tag
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("stop", "halt", "error")

    def process(self, ctx: Context) -> Optional[str]:
        if helper_parse_if(cast(str, ctx.verb.parameter)):
            raise StopError("" if ctx.verb.payload is None else ctx.verb.payload)
        return ""
