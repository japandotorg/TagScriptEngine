from __future__ import annotations

import random
from typing import Optional, Tuple, cast

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("RandomBlock",)


class RandomBlock(verb_required_block(True, payload=True)):  # type: ignore
    """
    Pick a random item from a list of strings, split by either ``~``
    or ``,``. An optional seed can be provided to the parameter to
    always choose the same item when using that seed.

    **Usage:** ``{random([seed]):<list>}``

    **Aliases:** ``#, rand``

    **Payload:** list

    **Parameter:** seed, None

    **Examples:** ::

        {random:Carl,Harold,Josh} attempts to pick the lock!
        # Possible Outputs:
        # Josh attempts to pick the lock!
        # Carl attempts to pick the lock!
        # Harold attempts to pick the lock!

        {=(insults):You're so ugly that you went to the salon and it took 3 hours just to get an estimate.~I'll never forget the first time we met, although I'll keep trying.~You look like a before picture.}
        {=(insult):{#:{insults}}}
        {insult}
        # Assigns a random insult to the insult variable
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("random", "#", "rand")

    def process(self, ctx: Context) -> Optional[str]:
        spl = []
        if "~" in (payload := cast(str, ctx.verb.payload)):
            spl = payload.split("~")
        else:
            spl = payload.split(",")
        random.seed(ctx.verb.parameter)

        return random.choice(spl)
