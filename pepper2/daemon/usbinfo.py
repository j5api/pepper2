"""USBInfo class."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass
class USBInfo:
    """Represents Information about an inserted USB."""

    dbus_job_path: str
    dbus_fs_path: str
    dbus_drive_path: str
    mount_path: Path