from __future__ import annotations

from typing import Tuple

from .discordadapters import (
    AttributeAdapter as AttributeAdapter,
    DiscordAttributeAdapter as DiscordAttributeAdapter,
    UserAdapter as UserAdapter,
    MemberAdapter as MemberAdapter,
    DMChannelAdapter as DMChannelAdapter,
    ChannelAdapter as ChannelAdapter,
    GuildAdapter as GuildAdapter,
    RoleAdapter as RoleAdapter,
    DiscordObjectAdapter as DiscordObjectAdapter,
)
from .functionadapter import (
    FunctionAdapter as FunctionAdapter,
)
from .intadapter import (
    IntAdapter as IntAdapter,
)
from .objectadapter import (
    SafeObjectAdapter as SafeObjectAdapter,
)
from .redbotadapters import (
    RedCommandAdapter as RedCommandAdapter,
    RedBotAdapter as RedBotAdapter,
)
from .stringadapter import (
    StringAdapter as StringAdapter,
)


__all__: Tuple[str, ...] = (
    "SafeObjectAdapter",
    "StringAdapter",
    "IntAdapter",
    "FunctionAdapter",
    "AttributeAdapter",
    "DiscordAttributeAdapter",
    "UserAdapter",
    "MemberAdapter",
    "DMChannelAdapter",
    "ChannelAdapter",
    "GuildAdapter",
    "RoleAdapter",
    "DiscordObjectAdapter",
    "RedCommandAdapter",
    "RedBotAdapter",
)
