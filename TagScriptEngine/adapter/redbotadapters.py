import datetime
from typing import Any, Dict, Optional, Tuple, cast

import discord

from ..verb import Verb
from ..interface import SimpleAdapter
from ..utils import escape_content

try:
    import redbot  # noqa: F401
except ModuleNotFoundError:
    _has_redbot = False
else:
    _has_redbot = True

    from redbot.core.bot import Red
    from redbot.core.commands import Command
    from redbot.core.utils.chat_formatting import humanize_number, humanize_list
    

__all__: Tuple[str, ...] = ("RedCommandAdapter", "RedBotAdapter")


class RedCommandAdapter(SimpleAdapter["Command"]):
    def __init__(self, base: Command, *, signature: Optional[str] = None) -> None:
        super().__init__(base=base)
        self.signature: Optional[str] = signature

        if not _has_redbot:
            raise ImportError("A Red-DiscordBot instance is required to use this.", name="redbot")

    def update_attributes(self) -> None:
        command: Command = self.object
        self._attributes.update(
            {
                "name": command.name,
                "cog_name": getattr(command, "cog_name", None),
                "description": getattr(command, "description", None),
                "aliases": humanize_list(list(getattr(command, "aliases", []))) or "None",
                "qualified_name": command.qualified_name,
                "signature": self.signature,
            }
        )

    def get_value(self, ctx: Verb) -> str:
        should_escape: bool = False
        if ctx.parameter is None:
            return_value: str = self.object.qualified_name
        else:
            try:
                value: Any = self._attributes[ctx.parameter]
            except KeyError:
                return  # type: ignore
            if isinstance(value, tuple):
                value, should_escape = value
            return_value: str = str(value) if value is not None else None  # type: ignore
        return escape_content(return_value) if should_escape else return_value


class RedBotAdapter(SimpleAdapter["Red"]):
    """
    The ``{bot}`` block with no parameters returns the bot's name & discriminator,
    but passing the attributes listed below to the block payload will return that attribute instead.

    **Usage:** ``{bot([attribute])}``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The bot's Discord ID.
    name
        The bot's username.
    discriminator
        The bot's discriminator.
    nick
        The bot's nickname, if they have one, else their username.
    created_at
        The bot's creation date.
    timestamp
        The bot's creation date as a UTC timestamp.
    mention
        A formatted text that pings the bot.
    verified
        If the bot is verified or not.
    shard_count (*)
        The bot's total shard count.
    servers (*)
        Total server/guild count of the bot.
    channels (*)
        Total number of channels visible to the bot.
    visible_users (*)
        Total number of users visible to the bot.
    total_users (*)
        The bot's total user count.
    unique_users (*)
        The bot's unique user count.
    percentage_chunked (*)
        Percentage of chunked guilds the bot has.

    .. warning::
        Attributes denoting `(*)` can only be used by the bot owner.
    """

    if not _has_redbot:
        raise ImportError("A Red-DiscordBot instance is required to use this.")

    def __init__(self, base: Red, *, owner: bool = True) -> None:
        super().__init__(base=base)
        self.is_owner: bool = owner

    def update_attributes(self) -> None:
        self.user: discord.ClientUser = cast(discord.ClientUser, self.object.user)
        created_at: datetime.datetime = getattr(
            self.user, "created_at", None
        ) or discord.utils.snowflake_time(self.user.id)
        self._attributes.update(
            {
                "id": self.user.id,
                "name": self.user.name,
                "discriminator": self.user.discriminator,
                "nick": self.user.display_name,
                "mention": self.user.display_avatar.url,
                "created_at": created_at,
                "timestamp": int(created_at.timestamp()),
                "verified": self.user.verified,
            }
        )
        if self.is_owner:
            visible_users: int = sum(len(g.members) for g in self.object.guilds)
            total_users: int = sum(
                g.member_count if g.member_count else 0 for g in self.object.guilds
            )
            owner_attributes: Dict[str, Any] = {
                "shard_count": humanize_number(self.object.bot.shard_count),
                "servers": humanize_number(len(self.object.guilds)),
                "channels": humanize_number(sum(len(g.channels) for g in self.object.guilds)),
                "visible_users": humanize_number(visible_users),
                "total_users": humanize_number(total_users),
                "unique_users": humanize_number(len(self.object.users)),
                "percentage_chunked": visible_users / total_users * 100,
            }
            self._attributes.update(owner_attributes)

    def get_value(self, ctx: Verb) -> str:
        should_escape: bool = False
        if ctx.parameter is None:
            return_value: str = "{0.name}#{0.discriminator}".format(self.user)
        else:
            try:
                value: Any = self._attributes[ctx.parameter]
            except KeyError:
                return  # type: ignore
            if isinstance(value, tuple):
                value, should_escape = value
            return_value: str = str(value) if value is not None else None  # type: ignore
        return escape_content(return_value) if should_escape else return_value
