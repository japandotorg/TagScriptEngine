from __future__ import annotations

from typing import Optional, Tuple, cast

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("RedirectBlock",)


class RedirectBlock(verb_required_block(True, parameter=True)):  # type: ignore
    """
    Redirects the tag response to either the given channel, the author's DMs,
    or uses a reply based on what is passed to the parameter.

    **Usage:** ``{redirect(<"dm"|"reply"|channel>)}``

    **Payload:** None

    **Parameter:** "dm", "reply", channel

    **Examples:** ::

        {redirect(dm)}
        {redirect(reply)}
        {redirect(#general)}
        {redirect(626861902521434160)}
    """

    ACCEPTED_NAMES = ("redirect",)

    def process(self, ctx: Context) -> Optional[str]:
        param: str = cast(str, ctx.verb.parameter).strip()
        if param.lower() == "dm":
            target: str = "dm"
        elif param.lower() == "reply":
            target: str = "reply"
        else:
            target = param
        ctx.response.actions["target"] = target
        return ""
