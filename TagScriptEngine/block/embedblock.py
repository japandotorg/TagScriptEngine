from __future__ import annotations

import json
from inspect import ismethod
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from discord import Colour, Embed

from ..interface import Block
from ..interpreter import Context
from .helpers import helper_split, easier_helper_split, implicit_bool
from ..exceptions import BadColourArgument, EmbedParseError
from .._warnings import removal

try:
    import orjson  # noqa: F401
except ModuleNotFoundError:
    _has_orjson: bool = False
else:
    _has_orjson: bool = True


__all__: Tuple[str, ...] = ("EmbedBlock",)


if _has_orjson:
    _from_json = orjson.loads  # type: ignore
else:
    _from_json = json.loads


def string_to_color(argument: str) -> Colour:
    arg = argument.replace("0x", "").lower()

    if arg[0] == "#":
        arg = arg[1:]
    try:
        value = int(arg, base=16)
        if not (0 <= value <= 0xFFFFFF):
            raise BadColourArgument(arg)
        return Colour(value=value)
    except ValueError:
        arg = arg.replace(" ", "_")
        method = getattr(Colour, arg, None)
        if arg.startswith("from_") or method is None or not ismethod(method):
            raise BadColourArgument(arg)
        return method()


def set_color(embed: Embed, attribute: str, value: str) -> None:
    value = string_to_color(value)  # type: ignore
    setattr(embed, attribute, value)


def set_dynamic_url(embed: Embed, attribute: str, value: str) -> None:
    method = getattr(embed, f"set_{attribute}")
    method(url=value)


def add_field(embed: Embed, _: str, payload: str) -> None:
    if (data := easier_helper_split(payload, maxsplit=3)) is None:  # type: ignore
        raise EmbedParseError("`add_field` payload was not split by |")
    try:
        name, value, _inline = data
        inline = implicit_bool(_inline)
        if inline is None:
            raise EmbedParseError(
                "`inline` argument for `add_field` is not a boolean value (_inline)"
            )
    except ValueError:
        name, value = cast(List[str], helper_split(payload, 2))  # type: ignore
        inline = False
    embed.add_field(name=name, value=value, inline=inline)


def set_footer(embed: Embed, _: str, payload: str) -> None:
    data = easier_helper_split(payload, maxsplit=2)  # type: ignore
    if data is None:
        embed.set_footer(text=payload)
    else:
        text, icon_url = data
        embed.set_footer(text=text, icon_url=icon_url)


class EmbedBlock(Block):
    """
    An embed block will send an embed in the tag response.
    There are two ways to use the embed block, either by using properly
    formatted embed JSON from an embed generator or manually inputting
    the accepted embed attributes.

    **JSON**

    Using JSON to create an embed offers complete embed customization.
    Multiple embed generators are available online to visualize and generate
    embed JSON.

    **Usage:** ``{embed(<json>)}``

    **Payload:** None

    **Parameter:** json

    **Examples:** ::

        {embed({"title":"Hello!", "description":"This is a test embed."})}
        {embed({
            "title":"Here's a random duck!",
            "image":{"url":"https://random-d.uk/api/randomimg"},
            "color":15194415
        })}

    **Manual**

    The following embed attributes can be set manually:

    *   ``title``
    *   ``description``
    *   ``color``
    *   ``url``
    *   ``thumbnail``
    *   ``image``
    *   ``footer``
    *   ``field`` - (See below)

    Adding a field to an embed requires the payload to be split by ``|``,
    ``;`` or ``,`` into either 2 or 3 parts. The first part is the name
    of the field, the  second is the text of the field, and the third
    optionally specifies  whether the field should be inline.

    **Usage:** ``{embed(<attribute>):<value>}``

    **Payload:** value

    **Parameter:** attribute

    **Examples:** ::

        {embed(color):#37b2cb}
        {embed(title):Rules}
        {embed(description):Follow these rules to ensure a good experience in our server!}
        {embed(field):Rule 1|Respect everyone you speak to.|false}
        {embed(footer):Thanks for reading!|{guild(icon)}}

    Both methods can be combined to create an embed in a tag.
    The following tagscript uses JSON to create an embed with fields and later
    set the embed title.

    ::

        {embed(title):my embed title}
        {embed({{
            "fields": [
                {
                    "name": "Field 1",
                    "value": "field description",
                    "inline": false
                }
            ]
        })}
    """

    ACCEPTED_NAMES: Tuple[str, ...] = ("embed",)

    ATTRIBUTE_HANDLERS: Dict[str, Any] = {
        "description": setattr,
        "title": setattr,
        "color": set_color,
        "colour": set_color,
        "url": setattr,
        "thumbnail": set_dynamic_url,
        "image": set_dynamic_url,
        "field": add_field,
        "footer": set_footer,
    }

    @removal(
        name="EmbedBlock",
        reason=(
            "One of EmbedBlock's trait is scheduled to be removed in the next minor release, "
            "A minor exception handling which would restrict the embed from getting sent and "
            "would raise TagScriptEngine.exceptions.EmbedParseError incase it had more than "
            "6000 characters, to know more about the limitations of discord embeds refer to the "
            "[Official Discord API Docs](https://discord.com/developers/docs/resources/channel#embed-object-embed-limits)."
        ),
        version="3.2.0",
    )
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_embed(ctx: Context) -> Embed:
        return ctx.response.actions.get("embed", Embed())

    @staticmethod
    def value_to_color(value: Optional[Union[int, str]]) -> Colour:
        if value is None or isinstance(value, Colour):
            return value  # type: ignore
        if isinstance(value, int):
            return Colour(value)
        elif isinstance(value, str):
            return string_to_color(value)
        else:
            raise EmbedParseError("Received invalid type for color key (expected string or int)")

    def text_to_embed(self, text: str) -> Embed:
        try:
            data = _from_json(text)
        except (json.decoder.JSONDecodeError, ValueError) as error:
            raise EmbedParseError(error) from error

        if data.get("embed"):
            data = data["embed"]
        if data.get("timestamp"):
            data["timestamp"] = data["timestamp"].strip("Z")

        color = data.pop("color", data.pop("colour", None))

        try:
            embed = Embed.from_dict(data)
        except Exception as error:
            raise EmbedParseError(error) from error
        else:
            if color := self.value_to_color(color):
                embed.color = color
            return embed

    @classmethod
    def update_embed(cls, embed: Embed, attribute: str, value: str) -> Embed:
        handler = cls.ATTRIBUTE_HANDLERS[attribute]
        try:
            handler(embed, attribute, value)
        except Exception as error:
            raise EmbedParseError(error) from error
        return embed

    @staticmethod
    def return_error(error: Exception) -> str:
        return f"Embed Parse Error: {error}"

    @staticmethod
    def return_embed(ctx: Context, embed: Embed) -> str:
        try:
            length = len(embed)
        except Exception as error:
            return str(error)
        if length > 6000:
            return f"`MAX EMBED LENGTH REACHED ({length}/6000)`"
        ctx.response.actions["embed"] = embed
        return ""

    def process(self, ctx: Context) -> Optional[str]:
        if not ctx.verb.parameter:
            return self.return_embed(ctx, self.get_embed(ctx))

        lowered = ctx.verb.parameter.lower()
        try:
            if ctx.verb.parameter.startswith("{") and ctx.verb.parameter.endswith("}"):
                embed = self.text_to_embed(ctx.verb.parameter)
            elif lowered in self.ATTRIBUTE_HANDLERS and ctx.verb.payload:
                embed = self.get_embed(ctx)
                embed = self.update_embed(embed, lowered, ctx.verb.payload)
            else:
                return
        except EmbedParseError as error:
            return self.return_error(error)

        return self.return_embed(ctx, embed)
