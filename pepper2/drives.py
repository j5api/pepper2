"""Classes to interact with drives."""

from enum import Enum
from pathlib import Path
from typing import Dict

DriveGroup = Dict[str, 'Drive']


class DriveType(Enum):
    """The Drive Type."""

    NO_ACTION = 0
    USERCODE = 1
    METADATA = 2
    SYSTEM_UPDATE = 3


class Drive:
    """An individual drive."""

    def __init__(
            self,
            *,
            uuid: str,
            mount_path: Path,
            drive_type: DriveType,
    ):
        self.uuid = uuid
        self.mount_path = mount_path
        self.drive_type = drive_type
