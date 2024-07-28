from __future__ import annotations

import logging
import datetime
from random import choice
from typing import Any, Dict, Union, cast, Tuple

import discord

from ..verb import Verb
from ..utils import escape_content
from .._warnings import deprecated
from ..interface import Adapter, SimpleAdapter


_log: logging.Logger = logging.getLogger(__name__)


__all__: Tuple[str, ...] = (
    "AttributeAdapter",
    "DiscordAttributeAdapter",
    "UserAdapter",
    "MemberAdapter",
    "DMChannelAdapter",
    "ChannelAdapter",
    "GuildAdapter",
    "RoleAdapter",
    "DiscordObjectAdapter",
)


class AttributeAdapter(Adapter):
    """
    .. deprecated:: 3.2.0
        AttributeAdapter has been deprecated and will be removed in favor of
        ``TagScriptEngine.adapter.discordadpaters.DiscordAttributeAdapter`` or
        consider using ``TagScriptEngine.interface.adapter.SimpleAdapter`` instead.
    """

    __slots__: Tuple[str, ...] = ("object", "_attributes", "_methods")

    @deprecated(
        name="TagScriptEngine.adapter.discordadpaters.AttributeAdapter",
        reason=(
            "AttributeAdapter has been deprecated and will be removed in favor of "
            "``TagScriptEngine.adapter.discordadpaters.DiscordAttributeAdapter`` or "
            "consider using ``TagScriptEngine.interface.adapter.SimpleAdapter`` instead."
        ),
        version="3.2.0",
    )
    def __init__(self, base: Union[discord.TextChannel, discord.Member, discord.Guild]) -> None:
        self.object: Union[discord.TextChannel, discord.Member, discord.Guild] = base
        created_at: datetime.datetime = getattr(
            base, "created_at", None
        ) or discord.utils.snowflake_time(base.id)
        self._attributes: Dict[str, Any] = {
            "id": base.id,
            "created_at": created_at,
            "timestamp": int(created_at.timestamp()),
            "name": getattr(base, "name", str(base)),
        }
        self._methods: Dict[str, Any] = {}
        self.update_attributes()
        self.update_methods()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} object={self.object!r}>"

    def update_attributes(self) -> None:
        pass

    def update_methods(self) -> None:
        pass

    def get_value(self, ctx: Verb) -> str:
        should_escape = False
        if ctx.parameter is None:
            return_value = str(self.object)
        else:
            try:
                value = self._attributes[ctx.parameter]
            except KeyError:
                if method := self._methods.get(ctx.parameter):
                    value = method()
                else:
                    return  # type: ignore
            if isinstance(value, tuple):
                value, should_escape = value
            return_value: str = str(value) if value is not None else None  # type: ignore
        return escape_content(return_value) if should_escape else return_value


class DiscordAttributeAdapter(
    SimpleAdapter[
        Union[
            discord.TextChannel,
            discord.DMChannel,
            discord.User,
            discord.Member,
            discord.Guild,
            discord.Role,
        ]
    ]
):
    """
    .. versionadded:: 3.2.0
    """

    def __init__(
        self,
        base: Union[
            discord.TextChannel,
            discord.DMChannel,
            discord.User,
            discord.Member,
            discord.Guild,
            discord.Role,
        ],
    ) -> None:
        super().__init__(base=base)
        created_at: datetime.datetime = getattr(
            base, "created_at", None
        ) or discord.utils.snowflake_time(base.id)
        self._attributes.update(
            {
                "id": base.id,
                "created_at": created_at,
                "timestamp": int(created_at.timestamp()),
                "name": getattr(base, "name", str(base)),
            }
        )

    def __repr__(self) -> str:
        return "<{} object={}>".format(type(self).__qualname__, self.object)

    def get_value(self, ctx: Verb) -> str:  # type: ignore
        should_escape = False
        if ctx.parameter is None:
            return_value = str(self.object)
        else:
            try:
                value = self._attributes[ctx.parameter]
            except KeyError:
                if method := self._methods.get(ctx.parameter):
                    value = method()
                else:
                    _log.debug(
                        "No parameter named `{}` found for the `{}` Adapter.".format(
                            ctx.parameter, self.__class__.__name__
                        )
                    )
                    return  # type: ignore
            if isinstance(value, tuple):
                value, should_escape = value
            return_value = str(value) if value is not None else None
        return escape_content(return_value) if should_escape else return_value  # type: ignore


class UserAdapter(DiscordAttributeAdapter):
    """
    The ``{user}`` block with no parameters returns the user's full username,
    but passing the attributes listed below to the block payload will return
    that attribute instead.

    **Usage:** ``{user([attribute])}``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The user's Discord ID.
    name
        The user's username.
    nick
        The user's nickname, if they have one, else their username.
    avatar
        A link to the user's avatar, which can be used in embeds.
    created_at
        The user's account creation date.
    timestamp
        The user's account creation date as UTC timestamp.
    mention
        A formatted text that ping's the user.
    bot
        Wheather or not the user is a bot.
    accent_color
        The user's accent color if banner is not present.
    avatar_decoration
        A link to the user's avatar decoration.

    .. versionadded:: 3.2.0
    """

    def update_attributes(self) -> None:
        object: discord.User = cast(discord.User, self.object)
        avatar_url: str = object.display_avatar.url
        if asset := object.avatar_decoration:
            decoration: Union[str, bool] = asset.with_format("png").url
        else:
            decoration: Union[str, bool] = False
        additional_attributes: Dict[str, Any] = {
            "nick": object.display_name,
            "mention": object.mention,
            "avatar": (avatar_url, False),
            "bot": object.bot,
            "accent_color": getattr(object, "accent_color", False),
            "avatar_decoration": decoration,
        }
        self._attributes.update(additional_attributes)


class MemberAdapter(DiscordAttributeAdapter):
    """
    The ``{author}`` block with no parameters returns the tag invoker's full username
    and discriminator, but passing the attributes listed below to the block payload
    will return that attribute instead.

    **Aliases:** ``user``

    **Usage:** ``{author([attribute])``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The author's Discord ID.
    name
        The author's username.
    nick
        The author's nickname, if they have one, else their username.
    avatar
        A link to the author's avatar, which can be used in embeds.
    discriminator
        The author's discriminator.
    created_at
        The author's account creation date.
    timestamp
        The author's account creation date as a UTC timestamp.
    joined_at
        The date the author joined the server.
    joinstamp
        The author's join date as a UTC timestamp.
    mention
        A formatted text that pings the author.
    bot
        Whether or not the author is a bot.
    color
        The author's top role's color as a hex code.
    top_role
        The author's top role.
    roleids
        A list of the author's role IDs, split by spaces.
    boost
        If the user has boosted, this will be the UTC timestamp of when they did,
        if not this will be empty.
    timed_out
        If the user is timed out, this will be the UTC timestamp of when they'll be untimed-out,
        if not timed out this will be empty.
    banner
        The users banner url
    """

    def update_attributes(self) -> None:
        object: discord.Member = cast(discord.Member, self.object)
        avatar_url: str = object.display_avatar.url
        joined_at: datetime.datetime = getattr(object, "joined_at", self.object.created_at)
        additional_attributes: Dict[str, Any] = {
            "color": object.color,
            "colour": object.color,
            "nick": object.display_name,
            "avatar": (avatar_url, False),
            "discriminator": object.discriminator,
            "joined_at": joined_at,
            "joinstamp": int(joined_at.timestamp()),
            "mention": object.mention,
            "bot": object.bot,
            "top_role": getattr(object, "top_role", ""),
            "boost": getattr(object, "premium_since", ""),
            "timed_out": getattr(object, "timed_out_until", ""),
            "banner": object.banner.url if object.banner else "",
        }
        if roleids := getattr(self.object, "_roles", None):
            additional_attributes["roleids"] = " ".join(str(r) for r in roleids)
        self._attributes.update(additional_attributes)


class DMChannelAdapter(DiscordAttributeAdapter):
    """
    The ``{channel}`` block with no parameters returns the channel's full name
    but passing the attributes listed below to the block payload will return
    the attribute instead.

    **Usage:** ``{channel([attribute])``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The channel's ID.
    name
        The channel's name.
    created_at
        The channel's creation date.
    timestamp
        The channel's creation date as a UTC timestamp.
    jump_url
        A link to the channel.

    .. versionadded:: 3.2.0
    """

    def update_attributes(self) -> None:
        if isinstance(self.object, discord.DMChannel):
            additional_attributes: Dict[str, Any] = {
                "jump_url": getattr(self.object, "jump_url", None)
            }
            self._attributes.update(additional_attributes)


class ChannelAdapter(DiscordAttributeAdapter):
    """
    The ``{channel}`` block with no parameters returns the channel's full name
    but passing the attributes listed below to the block payload
    will return that attribute instead.

    **Usage:** ``{channel([attribute])``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The channel's ID.
    name
        The channel's name.
    created_at
        The channel's creation date.
    timestamp
        The channel's creation date as a UTC timestamp.
    nsfw
        Whether the channel is nsfw.
    mention
        A formatted text that pings the channel.
    topic
        The channel's topic.
    category_id
        The category the channel is associated with.
        If no category channel, this will return empty.
    jump_url
        A link to the channel.

    .. versionchanged:: 3.2.0
        Added ``jump_url`` as a parameter.
    """

    def update_attributes(self) -> None:
        if isinstance(self.object, discord.TextChannel):
            additional_attributes: Dict[str, Any] = {
                "nsfw": self.object.nsfw,
                "mention": self.object.mention,
                "topic": self.object.topic or "",
                "slowmode": self.object.slowmode_delay,
                "category_id": self.object.category_id or "",
                "jump_url": self.object.jump_url or None,
            }
            self._attributes.update(additional_attributes)


class GuildAdapter(DiscordAttributeAdapter):
    """
    The ``{server}`` block with no parameters returns the server's name
    but passing the attributes listed below to the block payload
    will return that attribute instead.

    **Aliases:** ``guild``

    **Usage:** ``{server([attribute])``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The server's ID.
    name
        The server's name.
    icon
        A link to the server's icon, which can be used in embeds.
    created_at
        The server's creation date.
    timestamp
        The server's creation date as a UTC timestamp.
    member_count
        The server's member count.
    bots
        The number of bots in the server.
    humans
        The number of humans in the server.
    description
        The server's description if one is set, or "No description".
    random
        A random member from the server.
    vanity
        If guild has a vanity, this returns the vanity else empty.
    owner_id
        The server owner's id.
    mfa
        The server's mfa level.
    boosters
        The server's active booster count.
    boost_level
        The server's current boost level/tier.
    discovery_splash
        A link to the server's discovery splash.
    invite_splash
        A link to the server's invite splash.
    banner
        A link to the server's banner.

    .. versionchanged:: 3.2.0
        Added ``mfa``, ``boosters``, ``boost_level``,
        ``discovery_splash``, ``invite_splash`` & ``banner``.
    """

    def update_attributes(self) -> None:
        object: discord.Guild = cast(discord.Guild, self.object)
        guild: discord.Guild = object
        bots: int = 0
        humans: int = 0
        for m in guild.members:
            if m.bot:
                bots += 1
            else:
                humans += 1
        member_count: int = getattr(guild, "member_count", 0)
        icon_url: str = getattr(guild.icon, "url", "")
        additional_attributes: Dict[str, Any] = {
            "icon": (icon_url, False),
            "member_count": member_count,
            "members": member_count,
            "bots": bots,
            "humans": humans,
            "description": guild.description or "No description.",
            "vanity": guild.vanity_url_code or "No Vanity URL.",
            "owner_id": guild.owner_id or "",
            "mfa": guild.mfa_level,
            "boosters": guild.premium_subscription_count,
            "boost_level": guild.premium_tier,
            "discovery_splash": getattr(guild.discovery_splash, "url", False),
            "invite_splash": getattr(guild.splash, "url", False),
            "banner": getattr(guild.banner, "url", False),
        }
        self._attributes.update(additional_attributes)

    def update_methods(self) -> None:
        additional_methods: Dict[str, Any] = {"random": self.random_member}
        self._methods.update(additional_methods)

    def random_member(self) -> discord.Member:
        object: discord.Guild = cast(discord.Guild, self.object)
        return choice(object.members)


class RoleAdapter(DiscordAttributeAdapter):
    """
    The ``{role}`` block with no parameters returns the role's full name
    but passing the attributes listed below to the block payload will
    return that attribute instead.

    **Usage:** ``{role([attribute])}``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The role's ID.
    name
        The role's name.
    created_at
        The role's creation date.
    timestamp
        The role's creation date as a UTC timestamp.
    color
        The role's color.
    display_icon
        The role's icon.
    hoist
        Wheather the role is hoisted or not.
    managed
        Wheather the role is managed or not.
    mention
        A formatted text that pings the role.
    position
        The role's position.

    .. versionadded:: 3.2.0
    """

    def update_attributes(self) -> None:
        object: discord.Role = cast(discord.Role, self.object)
        additional_attributes: Dict[str, Any] = {
            "color": object.color,
            "display_icon": getattr(object.display_icon, "url", False),
            "hoist": object.hoist,
            "managed": object.managed,
            "mention": object.mention,
            "position": object.position,
        }
        self._attributes.update(additional_attributes)


class DiscordObjectAdapter(Adapter):
    """
    The ``{object}`` block with no parameters returs the discord object's ID,
    but passing the attributes listed below to the block payload will return
    that attribute instead.

    **Usage:** ``{object([attribute])}``

    **Payload:** None

    **Parameter:** attribute, None

    Attributes
    ----------
    id
        The object's Discord ID.
    created_at
        The object's creation date.
    timestamp
        The object's creation date as a UTC timestamp.

    .. versionadded:: 3.2.0
    """

    __slots__: Tuple[str, ...] = ("object", "_attributes", "_methods")

    def __init__(self, base: discord.Object) -> None:
        self.object: discord.Object = base
        created_at: datetime.datetime = getattr(
            base, "created_at", None
        ) or discord.utils.snowflake_time(base.id)
        self._attributes: Dict[str, Any] = {
            "id": base.id,
            "created_at": created_at,
            "timestamp": int(created_at.timestamp()),
        }
        self._methods: Dict[str, Any] = {}
        self.update_attributes()
        self.update_methods()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} object={self.object!r}>"

    def update_attributes(self) -> None:
        pass

    def update_methods(self) -> None:
        pass

    def get_value(self, ctx: Verb) -> str:  # type: ignore
        should_escape = False

        if ctx.parameter is None:
            return_value = str(self.object.id)
        else:
            try:
                value = self._attributes[ctx.parameter]
            except KeyError:
                if method := self._methods.get(ctx.parameter):
                    value = method()
                else:
                    return  # type: ignore

            if isinstance(value, tuple):
                value, should_escape = value

            return_value = str(value) if value is not None else None

        return escape_content(return_value) if should_escape else return_value  # type: ignore
