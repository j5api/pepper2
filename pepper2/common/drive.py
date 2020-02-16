"""Classes to interact with drives."""

from pathlib import Path
from typing import Type

from pepper2.common.drive_types import DriveType


class Drive:
    """An individual drive."""

    def __init__(
            self,
            *,
            uuid: str,
            mount_path: Path,
            drive_type: Type[DriveType],
    ):
        self._uuid = uuid
        self._mount_path = mount_path
        self._drive_type = drive_type

    @property
    def uuid(self) -> str:
        """The UUID of the drive."""
        return self._uuid

    @property
    def mount_path(self) -> Path:
        """The mount path of the drive."""
        return self._mount_path

    @property
    def drive_type(self) -> Type[DriveType]:
        """The DriveType class of this drive."""
        return self._drive_type

    @drive_type.setter
    def drive_type(self, drive_type: Type[DriveType]) -> None:
        """
        The DriveType class of this drive.

        A drivetype should only be changed if it is dangerous
        to use the drive otherwise.
        """
        self._drive_type = drive_type