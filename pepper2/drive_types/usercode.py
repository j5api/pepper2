"""Usercode Drive Type."""

from typing import TYPE_CHECKING

from pepper2.constraint import Constraint, FilePresentConstraint

from .drive_type import DriveType

if TYPE_CHECKING:
    from pepper2.daemon.controller import Controller
    from pepper2.drives import Drive


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("main.py")

    @classmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the mount action."""
        raise NotImplementedError

    @classmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the unmount/remove action."""
        raise NotImplementedError
