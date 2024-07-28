from typing import Optional, Tuple, cast

from ..interface import Block
from ..interpreter import Context
from ..verb import Verb


__all__: Tuple[str, ...] = ("ShortCutRedirectBlock",)


class ShortCutRedirectBlock(Block):
    def __init__(self, var_name: str) -> None:
        self.redirect_name: str = var_name

    def will_accept(self, ctx: Context) -> bool:  # type: ignore
        return cast(str, ctx.verb.declaration).isdigit()

    def process(self, ctx: Context) -> Optional[str]:
        blank: Verb = Verb()
        blank.declaration = self.redirect_name
        blank.parameter = ctx.verb.declaration
        ctx.verb = blank
        return None
