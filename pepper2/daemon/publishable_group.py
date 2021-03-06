"""A group of objects that are published to DBus."""

from typing import Any, Dict, Iterator, MutableMapping, NamedTuple, TypeVar

from gi.repository import GLib
from pydbus.auto_names import auto_bus_name, auto_object_path
from pydbus.bus import Bus
from pydbus.registration import ObjectRegistration

U = TypeVar("U")


class PublishedObject(NamedTuple):
    """
    An object published on the bus.

    We must ignore the type on this object, as we are unable to type it.
    """

    bus_path: str
    registration: ObjectRegistration
    object: Any  # type: ignore


class PublishableGroup(MutableMapping[str, U]):
    """
    A group of objects that are published to DBus.

    Objects are published to DBus when they are inserted into the group.
    Objects are removed from the bus when they are deleted.
    """

    def __init__(
            self,
            bus: Bus,
            *,
            base_path: str = "uk.org.j5.pepper2",
    ) -> None:
        self._bus = bus
        self._bus_path = auto_bus_name(base_path)
        self._dict: Dict[str, PublishedObject] = {}  # type: ignore

    def __setitem__(self, k: str, v: U) -> None:
        if k in self._dict.keys():
            raise KeyError("Objects in PublishableGroup cannot be overridden.")
        bus_path = auto_object_path(self._bus_path, k).replace('-', '_')

        try:
            registration = self._bus.register_object(bus_path, v, None)

            published_object = PublishedObject(
                bus_path=bus_path,
                registration=registration,
                object=v,
            )

            self._dict[k] = published_object
        except GLib.Error as e:
            raise ValueError("Unable to publish the object on DBus.") from e

    def __delitem__(self, k: str) -> None:
        published_object = self._dict.pop(k)
        try:
            published_object.registration.unregister()
        except GLib.Error as e:
            raise ValueError("Unable to remove the object from DBus.") from e

    def __getitem__(self, k: str) -> U:
        return self._dict[k].object  # type: ignore

    def __len__(self) -> int:
        return len(self._dict)

    def __iter__(self) -> Iterator[str]:
        return iter(self._dict)

    def __repr__(self) -> str:
        return repr({k: r.object for k, r in self._dict.items()})
