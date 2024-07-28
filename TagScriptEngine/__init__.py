from __future__ import annotations

from typing import Final, NamedTuple, Tuple

from .adapter import (
    SafeObjectAdapter as SafeObjectAdapter,
    StringAdapter as StringAdapter,
    IntAdapter as IntAdapter,
    FunctionAdapter as FunctionAdapter,
    DiscordAttributeAdapter as DiscordAttributeAdapter,
    UserAdapter as UserAdapter,
    MemberAdapter as MemberAdapter,
    DMChannelAdapter as DMChannelAdapter,
    ChannelAdapter as ChannelAdapter,
    GuildAdapter as GuildAdapter,
    RoleAdapter as RoleAdapter,
    AttributeAdapter as AttributeAdapter,
    DiscordObjectAdapter as DiscordObjectAdapter,
    RedCommandAdapter as RedCommandAdapter,
    RedBotAdapter as RedBotAdapter,
)
from .block import (
    implicit_bool as implicit_bool,
    helper_parse_if as helper_parse_if,
    helper_parse_list_if as helper_parse_list_if,
    helper_split as helper_split,
    AllowedMentionsBlock as AllowedMentionsBlock,
    AllBlock as AllBlock,
    AnyBlock as AnyBlock,
    AssignmentBlock as AssignmentBlock,
    BlacklistBlock as BlacklistBlock,
    BreakBlock as BreakBlock,
    SequentialGather as SequentialGather,
    CommandBlock as CommandBlock,
    EmbedBlock as EmbedBlock,
    FiftyFiftyBlock as FiftyFiftyBlock,
    IfBlock as IfBlock,
    LooseVariableGetterBlock as LooseVariableGetterBlock,
    MathBlock as MathBlock,
    OverrideBlock as OverrideBlock,
    PythonBlock as PythonBlock,
    RandomBlock as RandomBlock,
    RangeBlock as RangeBlock,
    RedirectBlock as RedirectBlock,
    ReplaceBlock as ReplaceBlock,
    RequireBlock as RequireBlock,
    ShortCutRedirectBlock as ShortCutRedirectBlock,
    StopBlock as StopBlock,
    StrfBlock as StrfBlock,
    StrictVariableGetterBlock as StrictVariableGetterBlock,
    SubstringBlock as SubstringBlock,
    URLEncodeBlock as URLEncodeBlock,
    UpperBlock as UpperBlock,
    LowerBlock as LowerBlock,
    CountBlock as CountBlock,
    LengthBlock as LengthBlock,
    CooldownBlock as CooldownBlock,
)
from .interface import (
    Adapter as Adapter,
    SimpleAdapter as SimpleAdapter,
    Block as Block,
    verb_required_block as verb_required_block,
)
from ._warnings import (
    TagScriptEngineDeprecationWarning as TagScriptEngineDeprecationWarning,
)
from .exceptions import (
    TagScriptError as TagScriptError,
    WorkloadExceededError as WorkloadExceededError,
    ProcessError as ProcessError,
    EmbedParseError as EmbedParseError,
    BadColourArgument as BadColourArgument,
    StopError as StopError,
    CooldownExceeded as CooldownExceeded,
)
from .interpreter import (
    Interpreter as Interpreter,
    AsyncInterpreter as AsyncInterpreter,
    Context as Context,
    Response as Response,
    Node as Node,
    build_node_tree as build_node_tree,
)
from .utils import (
    truncate as truncate,
    escape_content as escape_content,
    maybe_await as maybe_await,
)
from .verb import (
    Verb as Verb,
)


__all__: Tuple[str, ...] = (
    "implicit_bool",
    "helper_parse_if",
    "helper_parse_list_if",
    "helper_split",
    "AllBlock",
    "AnyBlock",
    "AssignmentBlock",
    "BlacklistBlock",
    "BreakBlock",
    "SequentialGather",
    "CommandBlock",
    "CooldownBlock",
    "EmbedBlock",
    "FiftyFiftyBlock",
    "IfBlock",
    "LooseVariableGetterBlock",
    "MathBlock",
    "OverrideBlock",
    "PythonBlock",
    "RandomBlock",
    "RangeBlock",
    "RedirectBlock",
    "ReplaceBlock",
    "RequireBlock",
    "ShortCutRedirectBlock",
    "StopBlock",
    "StrfBlock",
    "StrictVariableGetterBlock",
    "SubstringBlock",
    "URLEncodeBlock",
    "UpperBlock",
    "LowerBlock",
    "CountBlock",
    "LengthBlock",
    "SafeObjectAdapter",
    "StringAdapter",
    "IntAdapter",
    "FunctionAdapter",
    "RedCommandAdapter",
    "RedBotAdapter",
    "AttributeAdapter",
    "DiscordAttributeAdapter",
    "UserAdapter",
    "MemberAdapter",
    "DMChannelAdapter",
    "ChannelAdapter",
    "GuildAdapter",
    "RoleAdapter",
    "DiscordObjectAdapter",
    "Adapter",
    "SimpleAdapter",
    "Block",
    "verb_required_block",
    "TagScriptEngineDeprecationWarning",
    "TagScriptError",
    "WorkloadExceededError",
    "ProcessError",
    "EmbedParseError",
    "BadColourArgument",
    "StopError",
    "CooldownExceeded",
    "Interpreter",
    "AsyncInterpreter",
    "Context",
    "Response",
    "Node",
    "build_node_tree",
    "truncate",
    "escape_content",
    "maybe_await",
    "Verb",
    "__version__",
    "VersionInfo",
    "version_info",
)


__version__: Final[str] = "3.2.2"


class VersionNamedTuple(NamedTuple):
    major: int
    minor: int
    micro: int


class VersionInfo(VersionNamedTuple):
    """
    Version information.

    Attributes
    ----------
    major: int
        Major version number.
    minor: int
        Minor version number.
    micro: int
        Micro version number.
    """

    __slots__: Tuple[str, ...] = ()

    def __str__(self) -> str:
        """
        Returns a string representation of the version information.

        Returns
        -------
        str
            String representation of the version information.
        """
        return "{major}.{minor}.{micro}".format(**self._asdict())

    @classmethod
    def from_str(cls, version: str) -> "VersionInfo":
        """
        Returns a VersionInfo instance from a string.

        Parameters
        ----------
        version: str
            String representation of the version information.

        Returns
        -------
        VersionInfo
            Version information.
        """
        return cls(*map(int, version.split(".")))


version_info: VersionInfo = VersionInfo.from_str(__version__)
