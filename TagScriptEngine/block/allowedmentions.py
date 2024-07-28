from typing import Dict, List, Optional, Tuple, Union

from ..interface import Block
from ..interpreter import Context


class AllowedMentionsBlock(Block):
    """
    The ``{allowedmentions}`` block attempts to enable mentioning of roles.
    Passing no parameter enables mentioning of all roles within the message
    content. However passing a role name or ID to the block parameter allows
    mentioning of that specific role only. Multiple role name or IDs can be
    included, separated by a comma ",". By default, mentioning is only
    triggered if the execution author has "manage server" permissions. However,
    using the "override" keyword as a payload allows mentioning to be triggered
    by anyone.

    **Usage:** ``{allowedmentions(<role, None>):["override", None]}``

    **Aliases:** ``mentions``

    **Payload:** "override", None

    **Parameter:** role, None

    **Examples:** ::

        {allowedmentions}
        {allowedmentions:override}
        {allowedmentions(@Admin, Moderator):override}
        {allowedmentions(763522431151112265, 812949167190048769)}
        {mentions(763522431151112265, 812949167190048769):override}
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("allowedmentions", "mentions")
    PAYLOADS: Tuple[str, ...] = ("override",)

    @classmethod
    def will_accept(cls, ctx: Context) -> bool:
        if ctx.verb.payload and ctx.verb.payload not in cls.PAYLOADS:
            return False
        return super().will_accept(ctx)

    def process(self, ctx: Context) -> Optional[str]:
        actions: Optional[Dict[str, Union[bool, List[str]]]] = ctx.response.actions.get(
            "allowed_mentions", None
        )
        if actions:
            return None
        if not (param := ctx.verb.parameter):
            ctx.response.actions["allowed_mentions"] = {
                "mentions": True,
                "override": True if ctx.verb.payload else False,
            }
            return ""
        ctx.response.actions["allowed_mentions"] = {
            "mentions": [r.strip() for r in param.split(",")],
            "override": True if ctx.verb.payload else False,
        }
        return ""
