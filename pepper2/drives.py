"""Classes to interact with drives."""

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict, List, Type

from .constraint import Constraint, FilePresentConstraint, TrueConstraint

DriveGroup = Dict[str, 'Drive']


class DriveType(metaclass=ABCMeta):
    """The Drive Type."""

    name: str = "Unknown Drive"

    @classmethod
    @abstractmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        raise NotImplementedError

    # NO_ACTION = 0
    # USERCODE = 1
    # METADATA = 2
    # SYSTEM_UPDATE = 3


class UserCodeDriveType(DriveType):
    """A drive with usercode."""

    name: str = "USERCODE"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return FilePresentConstraint("main.py")


class NoActionDriveType(DriveType):
    """A drive for which we take no action."""

    name: str = "NO_ACTION"

    @classmethod
    def constraint_matcher(cls) -> Constraint:
        """Get the constraints for a drive to match this type."""
        return TrueConstraint()


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


# List of drive types, in priority order.
# The first one that matches will be selected.
DRIVE_TYPES: List[Type[DriveType]] = [
    UserCodeDriveType,
    NoActionDriveType,
]
