"""A group of objects that are published to DBus."""

from typing import Dict, Iterator, MutableMapping, TypeVar

from pydbus.auto_names import auto_bus_name, auto_object_path
from pydbus.bus import Bus

U = TypeVar("U")


class PublishableGroup(MutableMapping[str, U]):
    """A group of objects that are published to DBus."""

    def __init__(
            self,
            bus: Bus,
            sub_path: str,
            *,
            base_path: str = "uk.org.j5.pepper2",
    ) -> None:
        self._bus = bus
        self._bus_path = auto_bus_name(base_path + "." + sub_path)
        self._dict: Dict[str, U] = {}

    def __setitem__(self, k: str, v: U) -> None:
        self._dict[k] = v
        s = auto_object_path(self._bus_path, k)
        s = s.replace('-', '_')
        self._bus.register_object(s, v, None)

    def __delitem__(self, k: str) -> None:
        self._dict.pop(k)

    def __getitem__(self, k: str) -> U:
        return self._dict[k]

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[str]:
        return iter(self._dict)

    def __repr__(self) -> str:
        return repr(self._dict)
