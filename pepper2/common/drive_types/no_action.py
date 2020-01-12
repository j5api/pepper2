"""No Action Drive Type."""

from typing import TYPE_CHECKING

from pepper2.common.constraint import Constraint, TrueConstraint

from .drive_type import DriveType

if TYPE_CHECKING:
    from pepper2.daemon.dbus.controller import Controller
    from pepper2.common.drives import Drive


class NoActionDriveType(DriveType):
    """A drive for which we take no action."""

    name: str = "NO_ACTION"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return TrueConstraint()

    @classmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """
        Perform the mount action.

        In this case, do absolutely nothing.
        """
        pass

    @classmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """
        Perform the unmount action.

        In this case, do absolutely nothing.
        """
        pass
