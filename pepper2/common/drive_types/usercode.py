"""Usercode Drive Type."""

import logging
from typing import TYPE_CHECKING, Mapping, Type

from pepper2.common.constraint import (
    Constraint,
    FalseConstraint,
    FilePresentConstraint,
    OrConstraint,
)
from pepper2.daemon.usercode_driver import (
    PythonUnixProcessDriver,
    UserCodeDriver,
)

from .drive_type import DriveType

if TYPE_CHECKING:
    from pepper2.common.drive import Drive

LOGGER = logging.getLogger(__name__)

DRIVERS: Mapping[str, Type[UserCodeDriver]] = {
    "main.py": PythonUnixProcessDriver,
}


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        constraint: Constraint = FalseConstraint()

        for filename in DRIVERS.keys():
            constraint = OrConstraint(constraint, FilePresentConstraint(filename))

        return constraint

    @classmethod
    def mount_action(cls, drive: 'Drive') -> None:
        """Perform the mount action."""
        raise NotImplementedError("Mount action not implemented.")

    @classmethod
    def unmount_action(cls, drive: 'Drive') -> None:
        """Perform the unmount/remove action."""
        raise NotImplementedError("Unmount Action not implemented.")
