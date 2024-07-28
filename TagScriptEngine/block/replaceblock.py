from __future__ import annotations

from typing import Optional, Tuple, cast

from ..interface import verb_required_block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("ReplaceBlock", "PythonBlock")


class ReplaceBlock(verb_required_block(True, payload=True, parameter=True)):  # type: ignore
    """
    The replace block will replace specific characters in a string.
    The parameter should split by a ``,``, containing the characters to find
    before the command and the replacements after.

    **Usage:** ``{replace(<original,new>):<message>}``

    **Aliases:** ``None``

    **Payload:** message

    **Parameter:** original, new

    **Examples:** ::

        {replace(o,i):welcome to the server}
        # welcime ti the server

        {replace(1,6):{args}}
        # if {args} is 1637812
        # 6637862

        {replace(, ):Test}
        # T e s t
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("replace",)

    def process(self, ctx: Context) -> Optional[str]:
        try:
            before, after = cast(str, ctx.verb.parameter).split(",", 1)
        except ValueError:
            return

        return cast(str, ctx.verb.payload).replace(before, after)


class PythonBlock(verb_required_block(True, payload=True, parameter=True)):  # type: ignore
    """
    The in block serves three different purposes depending on the alias that is used.

    The ``in`` alias checks if the parameter is anywhere in the payload.

    ``contain`` strictly checks if the parameter is the payload, split by whitespace.

    ``index`` finds the location of the parameter in the payload, split by whitespace.
    If the parameter string is not found in the payload, it returns 1.

    index is used to return the value of the string form the given list of

    **Usage:** ``{in(<string>):<payload>}``

    **Aliases:** ``index``, ``contains``

    **Payload:** payload

    **Parameter:** string

    **Examples:** ::

        {in(apple pie):banana pie apple pie and other pie}
        # true
        {in(mute):How does it feel to be muted?}
        # true
        {in(a):How does it feel to be muted?}
        # false

        {contains(mute):How does it feel to be muted?}
        # false
        {contains(muted?):How does it feel to be muted?}
        # false

        {index(food):I love to eat food. everyone does.}
        # 4
        {index(pie):I love to eat food. everyone does.}
        # -1
    """

    def will_accept(self, ctx: Context) -> bool:  # type: ignore
        dec = cast(str, ctx.verb.declaration).lower()
        return dec in ("contains", "in", "index")

    def process(self, ctx: Context) -> str:
        dec: str = cast(str, ctx.verb.declaration).lower()
        if dec == "contains":
            return str(bool(ctx.verb.parameter in cast(str, ctx.verb.payload).split())).lower()
        elif dec == "in":
            return str(bool(cast(str, ctx.verb.parameter) in cast(str, ctx.verb.payload))).lower()
        else:
            try:
                return str(
                    cast(str, ctx.verb.payload)
                    .strip()
                    .split()
                    .index(cast(str, ctx.verb.parameter))
                )
            except ValueError:
                return "-1"
