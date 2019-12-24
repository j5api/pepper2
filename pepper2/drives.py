"""Classes to interact with drives."""

from pathlib import Path
from typing import Dict, Type

from .drive_types import DriveType

DriveGroup = Dict[str, 'Drive']


class Drive:
    """An individual drive."""

    def __init__(
            self,
            *,
            uuid: str,
            mount_path: Path,
            drive_type: Type[DriveType],
    ):
        self.uuid = uuid
        self.mount_path = mount_path
        self.drive_type = drive_type
