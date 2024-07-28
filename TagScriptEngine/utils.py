from __future__ import annotations

import re
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Tuple, TypeVar, Union


__all__: Tuple[str, ...] = ("truncate", "escape_content", "maybe_await")

T = TypeVar("T")

pattern: re.Pattern[str] = re.compile(r"(?<!\\)([{():|}])")


def _sub_match(match: re.Match) -> str:
    return "\\" + match[1]


def truncate(text: str, *, max: int = 2000, var: str = "...") -> str:
    """
    Truncate the given string to avoid hitting the character limit.

    Parameters
    ----------
    text
        The string to be truncated.
    max
        On what character length the string should be truncated.
    var
        The custom string used for trunication (defaults to '...').

    Returns
    -------
    str
        The truncated content.

    .. versionadded:: 3.2.0
    """
    if len(text) <= max:
        return text
    truncated: str = text[: max - 3]
    return truncated + var


def escape_content(string: str) -> str:
    """
    Escapes given input to avoid tampering with engine/block behavior.

    Returns
    -------
    str
        The escaped content.
    """
    if string is None:
        return
    return pattern.sub(_sub_match, string)


async def maybe_await(
    func: Callable[..., Union[T, Awaitable[T]]], *args: Any, **kwargs: Any
) -> Union[T, Any]:
    """
    Await the given function if it is awaitable or call it synchronously.

    Returns
    -------
    Any
        The result of the awaitable function.
    """
    value: Union[T, Awaitable[T]] = func(*args, **kwargs)
    return await value if isawaitable(value) else value
