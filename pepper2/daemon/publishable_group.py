"""A group of objects that are published to DBus."""

from typing import Any, Dict, Iterator, MutableMapping, NamedTuple, TypeVar

from pydbus.auto_names import auto_bus_name, auto_object_path
from pydbus.bus import Bus
from pydbus.registration import ObjectRegistration

U = TypeVar("U")


class PublishedObject(NamedTuple):
    """An object published on the bus."""

    bus_path: str
    registration: ObjectRegistration
    object: Any  # type: ignore


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
        self._dict: Dict[str, PublishedObject] = {}  # type: ignore

    def __setitem__(self, k: str, v: U) -> None:
        bus_path = auto_object_path(self._bus_path, k).replace('-', '_')
        registration = self._bus.register_object(bus_path, v, None)  # TODO: Try catch

        published_object = PublishedObject(
            bus_path=bus_path,
            registration=registration,
            object=v,
        )

        self._dict[k] = published_object

    def __delitem__(self, k: str) -> None:
        published_object = self._dict.pop(k)
        published_object.registration.unregister()

    def __getitem__(self, k: str) -> U:
        return self._dict[k].object  # type: ignore

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[str]:
        return iter(self._dict)

    def __repr__(self) -> str:
        return repr({k: r.object for k, r in self._dict.items()})
