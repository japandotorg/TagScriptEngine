import warnings
import functools
from typing import Callable, Optional, Tuple, TypeVar
from typing_extensions import ParamSpec


_P = ParamSpec("_P")
_T = TypeVar("_T")


__all__: Tuple[str, ...] = (
    "TagScriptEngineDeprecationWarning",
    "TagScriptEngineAttributeRemovalWarning",
)


class TagScriptEngineAttributeRemovalWarning(Warning):
    """A class for issuing removal warning for TagScriptEngine class attributes."""


class TagScriptEngineDeprecationWarning(DeprecationWarning):
    """A class for issuing deprecation warnings for TagScriptEngine modules."""


def remove(
    name: str, *, reason: Optional[str] = None, version: Optional[str] = None, level: int = 2
) -> None:
    warnings.warn(
        "Removal: {name}.{reason}{version}".format(
            name=name,
            reason=" ({})".format(reason) if reason else "",
            version=" -- Removal scheduled since version v{}".format(version) if version else "",
        ),
        category=TagScriptEngineAttributeRemovalWarning,
        stacklevel=level,
    )


def removal(
    *,
    name: Optional[str] = None,
    reason: Optional[str] = None,
    version: Optional[str] = None,
    level: int = 3,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def decorator(func: Callable[_P, _T]) -> Callable[_P, _T]:
        functools.wraps(func)

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            remove(name or func.__name__, reason=reason, version=version, level=level)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def depricate(
    name: str, *, reason: Optional[str] = None, version: Optional[str] = None, level: int = 2
) -> None:
    warnings.warn(
        "Deprecated: {name}.{reason}{version}".format(
            name=name,
            reason=" ({})".format(reason) if reason else "",
            version=" -- Deprecated since version v{}.".format(version) if version else "",
        ),
        category=TagScriptEngineDeprecationWarning,
        stacklevel=level,
    )


def deprecated(
    *,
    name: Optional[str] = None,
    reason: Optional[str] = None,
    version: Optional[str] = None,
    level: int = 3,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def decorator(func: Callable[_P, _T]) -> Callable[_P, _T]:
        functools.wraps(func)

        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            depricate(name or func.__name__, reason=reason, version=version, level=level)
            return func(*args, **kwargs)

        return wrapper

    return decorator
