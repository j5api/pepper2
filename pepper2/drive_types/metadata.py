"""Metadata Drive Type."""
from typing import TYPE_CHECKING

from pepper2.constraint import Constraint, FilePresentConstraint

from .drive_type import DriveType

if TYPE_CHECKING:
    from pepper2.daemon.controller import Controller
    from pepper2.drives import Drive


class MetadataDriveType(DriveType):
    """A drive with metadata."""

    name: str = "METADATA"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("pepper2.json")

    @classmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the mount action."""
        raise NotImplementedError

    @classmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the unmount/remove action."""
        raise NotImplementedError
