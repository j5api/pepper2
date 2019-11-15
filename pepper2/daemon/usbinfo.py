"""USBInfo class."""

from pathlib import Path
from typing import Dict


class USBInfo:
    """Represents Information about an inserted USB."""

    def __init__(self) -> None:
        pass

    @classmethod
    def from_dbus_data(cls, path: str, event_data: Dict[str, str]) -> 'USBInfo':
        """Create USBInfo from D-Bus data."""
        pass
