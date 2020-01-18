"""A group of objects that are published to DBus."""

from typing import Dict, Generic, Iterator, MutableMapping, TypeVar

from pydbus.bus import Bus

T = TypeVar("T")
U = TypeVar("U")


class PublishableGroup(MutableMapping[T, U], Generic[T, U]):
    """A group of objects that are published to DBus."""

    def __init__(self, bus: Bus) -> None:
        self._bus = bus
        self._dict: Dict[T, U] = {}

    def __setitem__(self, k: T, v: U) -> None:
        self._dict[k] = v

    def __delitem__(self, k: T) -> None:
        self._dict.pop(k)

    def __getitem__(self, k: T) -> U:
        return self._dict[k]

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[T]:
        return iter(self._dict)

    def __repr__(self) -> str:
        return repr(self._dict)
