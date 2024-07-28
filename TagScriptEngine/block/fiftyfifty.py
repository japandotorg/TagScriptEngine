from __future__ import annotations

import random
from typing import Optional, Tuple

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("FiftyFiftyBlock",)


class FiftyFiftyBlock(verb_required_block(True, payload=True)):  # type: ignore
    """
    The fifty-fifty block has a 50% change of returning the payload, and 50% chance of returning null.

    **Usage:**  ``{50:<message>}``

    **Aliases:**  ``5050, ?``

    **Payload:**  message

    **Parameter:**  None

    **Examples:**  ::

        I pick {if({5050:.}!=):heads|tails}
        # I pick heads
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("5050", "50", "?")

    def process(self, ctx: Context) -> Optional[str]:
        return random.choice(["", ctx.verb.payload])
