from typing import Optional

from ..interface import verb_required_block
from ..interpreter import Context


class UpperBlock(verb_required_block(True, payload=True)):
    """
    Converts the given text to uppercase.

    **Usage:** ``{upper:<string>}``

    **Aliases:** ``upper``

    **Payload:** ``string``

    **Parameter:** ``None``

    **Examples: **

    .. tagscript::

        {upper:ThiS is A Text}
        # THIS IS A TEXT
    """

    ACCEPTED_NAMES = "upper"

    def process(self, ctx: Context) -> Optional[str]:
        return ctx.verb.payload.upper()


class LowerBlock(verb_required_block(True, payload=True)):
    """
    Converts the given text to lowercase.

    **Usage:** ``{lower:<string>}``

    **Aliases:** ``lower``

    **Payload:** ``string``

    **Parameter:** ``None``

    **Examples: **

    .. tagscript::

        {upper:ThiS is A Text}
        # this is a text
    """

    ACCEPTED_NAMES = "lower"

    def process(self, ctx: Context) -> Optional[str]:
        return ctx.verb.payload.lower()
