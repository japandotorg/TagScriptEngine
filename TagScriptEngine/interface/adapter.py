from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, Protocol, Tuple, TypeVar

if TYPE_CHECKING:
    from ..verb import Verb


_T = TypeVar("_T", bound=object)


__all__: Tuple[str, ...] = ("Adapter", "SimpleAdapter")


class _Adapter(Protocol):
    def __repr__(self) -> str: ...

    def get_value(self, ctx: Verb) -> Optional[str]: ...


class Adapter(_Adapter):
    """
    The base class for TagScript blocks.

    Implementations must subclass this to create adapters.
    """

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} at {hex(id(self))}>"

    def get_value(self, ctx: Verb) -> Optional[str]:
        """
        Processes the adapter's actions for a given :class:`~TagScriptEngine.interpreter.Context`.

        Subclasses must implement this.

        Parameters
        ----------
        ctx: Verb
            The context object containing the TagScript :class:`~TagScriptEngine.verb.Verb`.

        Returns
        -------
        Optional[str]
            The adapters's processed value.

        Raises
        ------
        NotImplementedError
            The subclass did not implement this required method.
        """
        raise NotImplementedError


class SimpleAdapter(Adapter, Generic[_T]):
    __slots__: Tuple[str, ...] = ("object", "attributes", "_methods")

    def __init__(self, *, base: _T) -> None:
        self.object: _T = base
        self._attributes: Dict[str, Any] = {}
        self._methods: Dict[str, Any] = {}
        self.update_attributes()
        self.update_methods()

    def __repr__(self) -> str:
        return f"<{type(self).__qualname__} object={self.object!r}>"

    def update_attributes(self) -> None:
        pass

    def update_methods(self) -> None:
        pass

    def get_value(self, ctx: Verb) -> Optional[str]:
        raise NotImplementedError
