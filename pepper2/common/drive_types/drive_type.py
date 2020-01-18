"""Drive Type."""
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from pepper2.common.constraint import Constraint

if TYPE_CHECKING:
    from pepper2.daemon.dbus.controller import Controller
    from pepper2.daemon.dbus.drive import Drive


class DriveType(metaclass=ABCMeta):
    """
    The Drive Type.

    A drive type defines all of the behaviour of a specific drive.
    This includes:

    - Matching the drive
    - Special actions of the drive.
    """

    name: str = "Unknown Drive"

    @classmethod
    @abstractmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        raise NotImplementedError  # pragma: nocover

    @classmethod
    def start_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """
        Perform the start action.

        This is called on drives when pepperd is started and the drive is
        already inserted in the system. Defaults to calling the mount action.
        """
        cls.mount_action(drive, daemon_controller)

    @classmethod
    @abstractmethod
    def mount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the mount action."""
        raise NotImplementedError  # pragma: nocover

    @classmethod
    @abstractmethod
    def unmount_action(cls, drive: 'Drive', daemon_controller: 'Controller') -> None:
        """Perform the unmount/remove action."""
        raise NotImplementedError  # pragma: nocover
